from pipeline.merizo_adapter import run_merizo
from pyspark import SparkContext
from pyspark.sql import SparkSession
# import os
# from subprocess import Popen, PIPE
# from io import BytesIO

spark = SparkSession.builder.appName("MerizoSearch").getOrCreate()
sc = spark.sparkContext

# data_dir = "/test"

# def read_dir(input_dir, output_dir):
#     """
#     Function reads a fasta formatted file of protein sequences
#     """
#     print("Getting file list")
#     rdd = sc.wholeTextFiles(os.path.join(input_dir, "*.pdb"))
#     # file_ids = list(glob.glob(input_dir+"*.pdb"))
#     file_paths = rdd.keys().collect()
#     analysis_files = []
#     for file in file_paths:
#         id = os.path.basename(file)
#         analysis_files.append([file, id, output_dir])
#     return(analysis_files)

# def run_pipeline(input_dir, output_dir):
#     pdb_files = sc.binaryFiles(data_dir).map(lambda x: pipeline(BytesIO(x[1]), os.path.basename(x[0]), "/home/almalinux/")).collect()

#     print(pdb_files)

# run_pipeline(data_dir, "/home/almalinux/")

# Directory containing text files
input_directory = "/test"  # or a local path like "/path/to/directory"

# Read all text files in the directory
files_rdd = sc.wholeTextFiles(input_directory)
result = files_rdd.map(lambda x: run_merizo(x[0], x[1])).collect()

print(result)
