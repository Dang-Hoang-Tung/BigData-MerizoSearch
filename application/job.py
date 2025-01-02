from pipeline.merizo_adapter import run_merizo
from pyspark import SparkContext
from pyspark.sql import SparkSession
import os

spark = SparkSession.builder.appName("MerizoSearch").getOrCreate()
sc = spark.sparkContext

# Directory containing text files
dataset = "test"

def file_entry_mapper(file_entry):
    file_name = os.path.basename(file_entry[0])
    file_content = file_entry[1]
    return run_merizo(file_name, file_content, dataset)

# Read all text files in the directory
files_rdd = sc.wholeTextFiles(f'/{dataset}')
print("NUM_PARTITIONS: ", files_rdd.getNumPartitions())
repartitioned_rdd = files_rdd.repartition(11)
result = repartitioned_rdd.map(file_entry_mapper).reduce(lambda x, y: x)

print("ALL DONE")
