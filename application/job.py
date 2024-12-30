from pipeline.pipeline_script import run_test
from pyspark import SparkContext
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("MerizoSearch").getOrCreate()
sc = spark.sparkContext

data_dir = "/analysis_data/test"

filenames = run_test(sc, data_dir)

print("Outside")
print(filenames)
print("Done")

# results_human = analyse_spark("/analysis_data/UP000005640_9606_HUMAN_v4", sc, "arms")
# results_ecoli = analyse_spark("/analysis_data/UP000000625_83333_ECOLI_v4.tar", sc, "arms")

# data = []
# columns = ["year", "count"]
# for a in results.keys():
#     data.append([a, results[a]])
# df = spark.createDataFrame(data, columns).coalesce(1)
# df.show()
# df.write.option("header","true").mode("overwrite").csv("/1850_1859_sparksubmit")
