"""
Script to run the Merizo Search pipeline on a Spark cluster. Runs on the driver node.
This will distribute the tasks to worker nodes to process PDB files and collect the results.
"""

from pipeline.globals import *
from pipeline.merizo_adapter import merizo_adapter
from pyspark import SparkContext
from pyspark.sql import SparkSession
import os
from typing import List, Optional

spark = SparkSession.builder.appName(APPLICATION_NAME).getOrCreate()
sc = spark.sparkContext

spark_app_id = spark.sparkContext.applicationId
print(f"=== STARTING SPARK JOB - APP ID: {spark_app_id} ===")

def process_file(input_file_path: str, file_content: str, organism: str, dataset: str) -> Optional[AnalysisResults]:
    """
    Processes a PDB file in the dataset using the Merizo Search pipeline.
    """
    file_id = os.path.basename(input_file_path)
    return merizo_adapter(spark_app_id, file_id, file_content, organism, dataset)

def combine_means(n1, mean1, n2, mean2) -> float:
    """
    Calculates the new mean value based on the previous mean value and the new value.
    """
    return (n1 * mean1 + n2 * mean2) / (n1 + n2)

def combine_variance(n1, mean1, var1, n2, mean2, var2) -> float:
    """
    Calculates the new standard deviation value based on the previous mean and standard deviation values and the new values.
    """
    new_mean = combine_means(n1, mean1, n2, mean2)
    sum_sq_diff_1 = n1 * var1 + n1 * (mean1 - new_mean) ** 2
    sum_sq_diff_2 = n2 * var2 + n2 * (mean2 - new_mean) ** 2
    return (sum_sq_diff_1 + sum_sq_diff_2) / (n1 + n2)

def combine_plddt(plddt1: Plddt, plddt2: Plddt) -> Plddt:
    """
    Combines two Plddt objects into a single object.
    """
    return Plddt(
        size=plddt1.size + plddt2.size,
        mean=combine_means(plddt1.size, plddt1.mean, plddt2.size, plddt2.mean),
        variance=combine_variance(plddt1.size, plddt1.mean, plddt1.variance, plddt2.size, plddt2.mean, plddt2.variance)
    )

def combine_cath_code_tallies(tally1: CathCodeTally, tally2: CathCodeTally) -> CathCodeTally:
    """
    Combines two CathCodeTally objects into a single object.
    """
    new_tally = CathCodeTally()
    for key in list(tally1.keys()) + list(tally2.keys()):
        new_tally[key] = tally1.get(key, 0) + tally2.get(key, 0)
    return new_tally

def combine_results(dict_1: Optional[AnalysisResults], dict_2: Optional[AnalysisResults]) -> Optional[AnalysisResults]:
    """
    Combines the results from two dictionaries returned by worker tasks into a single dictionary.
    """
    if dict_1 and dict_2:
        return AnalysisResults(
            organism=dict_1.organism,
            plddt=combine_plddt(dict_1.plddt, dict_2.plddt),
            cath_code_tally=combine_cath_code_tallies(dict_1.cath_code_tally, dict_2.cath_code_tally)
        )
    elif dict_1:
        return dict_1
    elif dict_2:
        return dict_2
    else:
        return None

def distribute_tasks(organism: str, dataset: str, hdfs_dir: str, min_partitions: int) -> Optional[AnalysisResults]:
    """
    Distributes tasks to process files in the dataset. Each task is handled by a worker.
    The result is reduced to a single dictionary containing the  {cath_code: count} results and the list of mean plddt values.
    """
    rdd = sc.wholeTextFiles(hdfs_dir, minPartitions=min_partitions)
    print(f"=== {dataset}_NUM_PARTITIONS: {rdd.getNumPartitions()} ===")
    mapper = lambda x: process_file(x[0], x[1], organism, dataset)
    return rdd.map(mapper).reduce(combine_results)

def write_summary_to_file(results: AnalysisResults, output_file_path: str) -> None:
    """
    Writes the summary of the {cath_code: count} results to a CSV file.
    """
    column_headers = ["cath_code", "count"]
    data = [[key, value] for key, value in results.cath_code_tally.items()]
    sorted_data = sorted(data, key=lambda x: x[0])
    df = spark.createDataFrame(sorted_data, column_headers).coalesce(1)
    df.write.option("header", "true").mode("overwrite").csv(output_file_path)
    df.show()

def write_plddt_means_to_file(data: List[AnalysisResults], output_file_path: str) -> None:
    """
    Writes the mean and standard deviation of the plddt values to a CSV file.
    Args:
        data: list of lists, representing data rows in the format [<organism>, <mean>, <stdev>]
        output_file_path: the path to the output file
    """
    column_headers = ["organism", "mean plddt", "plddt std"]
    df_data = [[d.organism, d.plddt.mean, d.plddt.variance ** 0.5] for d in data]
    df = spark.createDataFrame(df_data, column_headers).coalesce(1)
    df.write.option("header", "true").mode("overwrite").csv(output_file_path)
    df.show()

def run_analysis(job_inputs: JobInputs) -> AnalysisResults:
    """
    Runs the analysis job on the specified dataset and writes the results to the output files.
    """
    # Distribute tasks to workers and collect the results
    results = distribute_tasks(job_inputs.organism, job_inputs.dataset, job_inputs.hdfs_dir, job_inputs.min_partitions)
    if (results):
        write_summary_to_file(results, job_inputs.summary_output_path)
        write_plddt_means_to_file([results], job_inputs.means_output_path)
        return results
    else:
        return AnalysisResults()

# # Testing the functionality
run_analysis(TEST_JOB_INPUTS)

# Process the ECOLI dataset
ecoli_results = run_analysis(ECOLI_JOB_INPUTS)

# Process the HUMAN dataset
# human_results = run_analysis(HUMAN_JOB_INPUTS)

# Write the combined means data to a file
# write_plddt_means_to_file([human_results, ecoli_results], COMBINED_MEANS_OUTPUT_PATH)

print("=== SPARK JOB COMPLETED SUCCESSFULLY - APP ID {app_id} ===")
