"""
Script to run the Merizo Search pipeline on a Spark cluster. Runs on the driver node.
This will distribute the tasks to worker nodes to process PDB files and collect the results.
"""

from global_vars import *
from pipeline.merizo_adapter import merizo_adapter
from pyspark import SparkContext
from pyspark.sql import SparkSession
import os
from statistics import mean, pstdev
from typing import List

spark = SparkSession.builder.appName(APPLICATION_NAME).getOrCreate()
sc = spark.sparkContext

def process_file(input_file_path: str, file_content: str, dataset: str) -> AnalysisResults:
    """
    Processes a PDB file in the dataset using the Merizo Search pipeline.
    """
    file_id = os.path.basename(input_file_path)
    return merizo_adapter(file_id, file_content, dataset)

def combine_results(acc_dict: AnalysisResults, new_dict: AnalysisResults) -> AnalysisResults:
    """
    Combines the results from two dictionaries returned by worker tasks into a single dictionary.
    """
    for key in new_dict:
        # Accumulate the mean plddt values
        if key == AnalysisResults.MEAN_PLDDT_KEY:
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

def distribute_tasks(dataset: str, hdfs_dir: str) -> AnalysisResults:
    """
    Distributes tasks to process files in the dataset. Each task is handled by a worker.
    The result is reduced to a single dictionary containing the  {cath_code: count} results and the list of mean plddt values.
    """
    rdd = sc.wholeTextFiles(hdfs_dir, minPartitions=MIN_PARTITIONS)
    print(f"=== {dataset}_NUM_PARTITIONS: {rdd.getNumPartitions()} ===")
    processor = lambda x: process_file(x[0], x[1], dataset)
    return rdd.map(processor).reduce(combine_results)

def write_summary_to_file(results: dict, output_file_path: str) -> None:
    """
    Writes the summary of the {cath_code: count} results to a CSV file.
    """
    data = []
    column_headers = ["cath_code", "count"]
    for key in results.keys():
        if key != AnalysisResults.MEAN_PLDDT_KEY:
            data.append([key, results[key]])
    sorted_data = sorted(data, key=lambda x: x[1])
    df = spark.createDataFrame(sorted_data, column_headers).coalesce(1)
    df.write.option("header", "true").mode("overwrite").csv(output_file_path)
    df.show()

def get_plddt_means(organism: str, means_list: List[float]) -> PlddtMeans:
    """
    Calculates the mean and standard deviation of the plddt values for the organism.
    Args:
        organism: the organism name
        means_list: the list of plddt mean values
    Returns:
        a PlddtMeans tuple
    """
    mean_value = mean(means_list)
    stdev_value = pstdev(means_list)
    return PlddtMeans(organism=organism, mean=mean_value, stdev=stdev_value)

def write_plddt_means_to_file(means_data: List[PlddtMeans], output_file_path: str) -> None:
    """
    Writes the mean and standard deviation of the plddt values to a CSV file.
    Args:
        data: list of lists, representing data rows in the format [<organism>, <mean>, <stdev>]
        output_file_path: the path to the output file
    """
    column_headers = ["organism", "mean plddt", "plddt std"]
    df_data = [[d.organism, d.mean, d.stdev] for d in means_data]
    df = spark.createDataFrame(df_data, column_headers).coalesce(1)
    df.write.option("header", "true").mode("overwrite").csv(output_file_path)
    df.show()

def run_analysis(job_inputs: JobInputs) -> PlddtMeans:
    """
    Runs the analysis job on the specified dataset and writes the results to the output files.
    """
    # Distribute tasks to workers and collect the results
    results = distribute_tasks(job_inputs.dataset, job_inputs.hdfs_dir)
    write_summary_to_file(results, job_inputs.summary_output_path)

    # Calculate the mean and standard deviation of the plddt values
    means_data = get_plddt_means(job_inputs.organism, results.mean_plddt_list)
    write_plddt_means_to_file([means_data], job_inputs.means_output_path)
    return means_data

# Testing the functionality
run_analysis(TEST_JOB_INPUTS)

# Process the ECOLI dataset
ecoli_means_data = run_analysis(ECOLI_JOB_INPUTS)

# Process the HUMAN dataset
human_means_data = run_analysis(HUMAN_JOB_INPUTS)

# Write the combined means data to a file
combined_means_df = write_plddt_means_to_file([human_means_data, ecoli_means_data], COMBINED_MEANS_OUTPUT_PATH)

print("=== SPARK JOB COMPLETED SUCCESSFULLY! ===")
