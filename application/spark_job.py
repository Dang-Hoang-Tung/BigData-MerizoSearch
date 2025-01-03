from pipeline.merizo_adapter import merizo_adapter
from pyspark import SparkContext
from pyspark.sql import SparkSession, functions as F
import os

spark = SparkSession.builder.appName("MerizoSearch").getOrCreate()
sc = spark.sparkContext

# Directory containing text files
TEST_DATASET = "test"
TEST_DATASET_HDFS_DIR = f'/{TEST_DATASET}'
TEST_SUMMARY_OUTPUT_PATH = "/test_cath_summary.csv"
TEST_MEANS_OUTPUT_PATH = "/test_plDDT_means.csv"

ECOLI_DATASET = "UP000000625_83333_ECOLI_v4"
ECOLI_DATASET_HDFS_DIR = f"/{ECOLI_DATASET}"
ECOLI_SUMMARY_OUTPUT_PATH = "/ecoli_cath_summary.csv"

HUMAN_DATASET = "UP000005640_9606_HUMAN_v4"
HUMAN_DATASET_HDFS_DIR = f"/{HUMAN_DATASET}"
HUMAN_SUMMARY_OUTPUT_PATH = "/human_cath_summary.csv"

PLDDT_MEANS_OUTPUT_PATH = "/plDDT_means.csv"

MEAN_PLDDT_KEY = "__MEAN_PLDDT__"

def process_file(file_entry, dataset: str):
    file_id = os.path.basename(file_entry[0])
    file_content = file_entry[1]
    return merizo_adapter(file_id, file_content, dataset, MEAN_PLDDT_KEY)

def combine_dict(acc_dict: dict, new_dict: dict):
    for key in new_dict:
        # Accumulate the mean plddt values
        if key == MEAN_PLDDT_KEY:
            if key in acc_dict:
                acc_dict[key].extend(new_dict[key])
            else:
                acc_dict[key] = new_dict[key]
        # Accumulate the counts for each cath_id
        else:
            if key in acc_dict:
                acc_dict[key] += new_dict[key]
            else:
                acc_dict[key] = new_dict[key]
    return acc_dict

def distribute_tasks(dataset: str, dataset_hdfs_dir: str):
    rdd = sc.wholeTextFiles(dataset_hdfs_dir, minPartitions=22)
    print(f"=== {dataset}_NUM_PARTITIONS: {rdd.getNumPartitions()} ===")
    process = lambda x: process_file(x, dataset)
    return rdd.map(process).reduce(combine_dict)

def write_summary_to_file(results: dict, file_path: str):
    data = []
    column_headers = ["cath_code", "count"]
    for a in results.keys():
        if a != MEAN_PLDDT_KEY:
            data.append([a, results[a]])
    sorted_data = sorted(data, key=lambda x: x[1])
    df = spark.createDataFrame(sorted_data, column_headers).coalesce(1)
    df.write.option("header","true").mode("overwrite").csv(file_path)
    return df

def get_plddt_means(means_data: list):
    column_headers = [MEAN_PLDDT_KEY]
    df = spark.createDataFrame(means_data, column_headers)
    [mean, stddev] = df.select(
        F.mean(MEAN_PLDDT_KEY).alias('mean'),
        F.stddev_pop(MEAN_PLDDT_KEY).alias('stddev')
    ).collect()[0]
    return [mean, stddev]

def write_plddt_means_to_file(ecoli_means_data: list, human_means_data: list, file_path: str):
    [ecoli_mean, ecoli_stddev] = get_plddt_means(ecoli_means_data)
    [human_mean, human_stddev] = get_plddt_means(human_means_data)

    column_headers = ["organism", "mean plddt", "plddt std"]
    data = [
        ["human", human_mean, human_stddev],
        ["ecoli", ecoli_mean, ecoli_stddev]
    ]
    df = spark.createDataFrame(data, column_headers).coalesce(1)
    df.write.option("header","true").mode("overwrite").csv(file_path)
    return df

# TESTING THE FUNCTIONALITY
# test_results = distribute_tasks(TEST_DATASET, TEST_DATASET_HDFS_DIR)
# test_summary_df = write_summary_to_file(test_results, TEST_SUMMARY_OUTPUT_PATH)
# test_summary_df.show()
# test_means_df = write_plddt_means_to_file(test_results[MEAN_PLDDT_KEY], test_results[MEAN_PLDDT_KEY], TEST_MEANS_OUTPUT_PATH)
# test_means_df.show()

# Process the ECOLI dataset
ecoli_results = distribute_tasks(ECOLI_DATASET, ECOLI_DATASET_HDFS_DIR)
ecoli_summary_df = write_summary_to_file(ecoli_results, ECOLI_SUMMARY_OUTPUT_PATH)
ecoli_summary_df.show()

# Process the HUMAN dataset
human_results = distribute_tasks(HUMAN_DATASET, HUMAN_DATASET_HDFS_DIR)
human_summary_df = write_summary_to_file(human_results, HUMAN_SUMMARY_OUTPUT_PATH)
human_summary_df.show()

combined_means_df = write_plddt_means_to_file(ecoli_results[MEAN_PLDDT_KEY], human_results[MEAN_PLDDT_KEY], PLDDT_MEANS_OUTPUT_PATH)
combined_means_df.show()

print("ALL DONE")
