import sys
from subprocess import Popen, PIPE
import glob
import os
import multiprocessing
from pyspark import SparkContext
from pyspark.sql import SparkSession

"""
usage: python pipeline_script.py [INPUT DIR] [OUTPUT DIR]
approx 5seconds per analysis
"""

spark = SparkSession.builder.appName("MerizoSearch").getOrCreate()
sc = spark.sparkContext

def run_parser(input_file, output_dir):
    """
    Run the results_parser.py over the hhr file to produce the output summary
    """
    search_file = input_file+"_search.tsv"
    print(search_file, output_dir)
    cmd = ['python', './results_parser.py', output_dir, search_file]
    print(f'STEP 2: RUNNING PARSER: {" ".join(cmd)}')
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))

def run_merizo_search(input_file, id):
    """
    Runs the merizo domain predictor to produce domains
    """
    cmd = ['python3',
           '/home/almalinux/merizo_search/merizo_search/merizo.py',
           'easy-search',
           input_file,
           '/home/almalinux/cath_foldclassdb/cath-4.3-foldclassdb',
           id,
           'tmp',
           '--iterate',
           '--output_headers',
           '-d',
           'cpu',
           '--threads',
           '1'
           ]
    print(f'STEP 1: RUNNING MERIZO: {" ".join(cmd)}')
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))
    
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

def pipeline(filepath, id, outpath):
    # STEP 1
    run_merizo_search(filepath, id)
    # STEP 2
    run_parser(id, outpath)

def run_pipeline(input_dir, output_dir):
    # print(sys.argv[1], sys.argv[2])
    pdbfiles = read_dir(input_dir, output_dir)
    print(pdbfiles)
    rdd = spark.sparkContext.parallelize(pdbfiles)
    results = rdd.map(lambda x: pipeline(x[0], x[1], x[2])).collect()
    print(results)
    print("DONE")

if __name__ == "__main__":
    print(sys.argv[1], sys.argv[2])
    pdbfiles = read_dir(sys.argv[1])
    print(pdbfiles)
    # rdd = spark.sparkContext.parallelize(pdbfiles)
    # rdd.map(lambda x: pipeline(x[0], x[1], x[2])).collect()
    # p = multiprocessing.Pool(1)
    # p.starmap(pipeline, pdbfiles[:10])

        