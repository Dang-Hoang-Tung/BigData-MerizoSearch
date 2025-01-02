from pipeline.merizo_adapter import merizo_adapter
from pyspark import SparkContext
from pyspark.sql import SparkSession
import os

spark = SparkSession.builder.appName("MerizoSearch").getOrCreate()
sc = spark.sparkContext

# Directory containing text files
dataset = "test"
input_dir = f'/{dataset}'

def file_entry_mapper(file_entry):
    file_name = os.path.basename(file_entry[0])
    file_content = file_entry[1]
    return merizo_adapter(file_name, file_content, dataset)

# Read all text files in the directory
files_rdd = sc.wholeTextFiles(input_dir)
print("NUM_PARTITIONS: ", files_rdd.getNumPartitions())
repartitioned_rdd = files_rdd.repartition(22)
result = repartitioned_rdd.map(file_entry_mapper).reduce(lambda x, y: x)

print("ALL DONE")
