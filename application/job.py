from pipeline.pipeline_script import pipeline
from pyspark import SparkContext
from pyspark.sql import SparkSession
import os
from subprocess import Popen, PIPE

spark = SparkSession.builder.appName("MerizoSearch").getOrCreate()
sc = spark.sparkContext

data_dir = "/test"

# filenames = run_test(sc, data_dir)

# print("Outside")
# print(filenames)
# print("Done")

# pipeline('/test/AF-Q46871-F1-model_v4.pdb', 'AF-Q46871-F1-model_v4.pdb', "~/output")
# print("Done 1")

# cmd = ['python', 'pipeline/pipeline_script.py', data_dir, 'file:///home/almalinux/output/']
# print(f'STEP 0: RUNNING PIPELINE: {" ".join(cmd)}')
# p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
# out, err = p.communicate()
# print(out.decode("utf-8"))
# print("Done 2")

def read_dir(input_dir, output_dir):
    """
    Function reads a fasta formatted file of protein sequences
    """
    print("Getting file list")
    rdd = sc.wholeTextFiles(os.path.join(input_dir, "*.pdb"))
    # file_ids = list(glob.glob(input_dir+"*.pdb"))
    file_paths = rdd.keys().collect()
    analysis_files = []
    for file in file_paths:
        id = os.path.basename(file)
        analysis_files.append([file, id, output_dir])
    return(analysis_files)

def run_pipeline(input_dir, output_dir):
    # print(sys.argv[1], sys.argv[2])
    pdbfiles = read_dir(input_dir, output_dir)
    print(pdbfiles)
    rdd = spark.sparkContext.parallelize(pdbfiles)
    print(rdd)
    print("STARTING")
    results = rdd.map(lambda x: pipeline(x[0], x[1], x[2])).collect()
    print(results)
    print("DONE")

run_pipeline(data_dir, "/home/almalinux/")

# results_human = analyse_spark("/analysis_data/UP000005640_9606_HUMAN_v4", sc, "arms")
# results_ecoli = analyse_spark("/analysis_data/UP000000625_83333_ECOLI_v4.tar", sc, "arms")

# data = []
# columns = ["year", "count"]
# for a in results.keys():
#     data.append([a, results[a]])
# df = spark.createDataFrame(data, columns).coalesce(1)
# df.show()
# df.write.option("header","true").mode("overwrite").csv("/1850_1859_sparksubmit")

