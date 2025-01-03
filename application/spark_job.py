from pipeline.merizo_adapter import merizo_adapter
from pyspark import SparkContext
from pyspark.sql import SparkSession
import os
from statistics import mean, pstdev

spark = SparkSession.builder.appName("MerizoSearch").getOrCreate()
sc = spark.sparkContext

# Directory containing text files
TEST_DATASET = "test"
TEST_DATASET_HDFS_DIR = f'/{TEST_DATASET}'
TEST_SUMMARY_OUTPUT_PATH = "/test_cath_summary.csv"

ECOLI_DATASET = "UP000000625_83333_ECOLI_v4"
ECOLI_DATASET_HDFS_DIR = f"/{ECOLI_DATASET}"
ECOLI_SUMMARY_OUTPUT_PATH = "/ecoli_cath_summary.csv"

HUMAN_DATASET = "UP000005640_9606_HUMAN_v4"
HUMAN_DATASET_HDFS_DIR = f"/{HUMAN_DATASET}"
HUMAN_SUMMARY_OUTPUT_PATH = "/human_cath_summary.csv"

MEAN_PLDDT_KEY = "__MEAN_PLDDT__"
PLDDT_MEANS_OUTPUT_PATH = "/plDDT_means.csv"

def process_file(file_entry, dataset: str):
    file_id = os.path.basename(file_entry[0])
    file_content = file_entry[1]
    return merizo_adapter(file_id, file_content, dataset, MEAN_PLDDT_KEY)

def combine_dict(acc_dict: dict, new_dict: dict):
    for key in new_dict:
        # Accumulate the mean plddt values
        if key == MEAN_PLDDT_KEY:
            if key in acc_dict:
                acc_dict[key].append(new_dict[key])
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
    columns = ["cath_code", "count"]
    for a in results.keys():
        if a != MEAN_PLDDT_KEY:
            data.append([a, results[a]])
    df = spark.createDataFrame(data, columns).coalesce(1).sort("cath_code")
    df.write.option("header","true").mode("overwrite").csv(file_path)
    return df

def write_mean_plddt_to_file(ecoli_means: list, human_means: list, file_path: str):
    columns = ["organism", "mean plddt", "plddt std"]
    data = [['human', str(mean(human_means)), str(pstdev(human_means))], ['ecoli', str(mean(ecoli_means)), str(pstdev(ecoli_means))]]
    df = spark.createDataFrame(data, columns).coalesce(1)
    df.write.option("header","true").mode("overwrite").csv(file_path)
    return df

test_results = distribute_tasks(TEST_DATASET, TEST_DATASET_HDFS_DIR)
test_summary_df = write_summary_to_file(test_results, TEST_SUMMARY_OUTPUT_PATH)
test_summary_df.show()
test_means_df = write_mean_plddt_to_file(test_results[MEAN_PLDDT_KEY], test_results[MEAN_PLDDT_KEY], PLDDT_MEANS_OUTPUT_PATH)
test_means_df.show()

# # Process the ECOLI dataset
# ecoli_results = distribute_tasks(ECOLI_DATASET, ECOLI_DATASET_HDFS_DIR)

# # Process the HUMAN dataset
# human_results = distribute_tasks(HUMAN_DATASET, HUMAN_DATASET_HDFS_DIR)

print("ALL DONE")
