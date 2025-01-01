import sys
from subprocess import Popen, PIPE
import glob
import os
import multiprocessing

"""
usage: python pipeline_script.py [INPUT DIR] [OUTPUT DIR]
approx 5seconds per analysis
"""

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
    # print(out.decode("utf-8"))
    # print(err.decode("utf-8"))

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
        #    '--output=/home/almalinux/',
        #    '--merizo_output=/home/almalinux/',
           ]
    print(f'STEP 1: RUNNING MERIZO: {" ".join(cmd)}')
    p = Popen(cmd, stdin=PIPE,stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))
    return [out.decode("utf-8"), err.decode("utf-8")]

def pipeline(filepath, id, outpath):
    # Get the current working directory
    current_directory = os.getcwd()
    print(f"Current Working Directory: {current_directory}")

    # Get the directory of the currently running script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"Script Directory: {script_directory}")
    # STEP 1
    res = run_merizo_search(filepath, id)
    # STEP 2
    run_parser(id, outpath)
    return [current_directory, res]

# if __name__ == "__main__":
#     print(sys.argv[1], sys.argv[2])
#     pdbfiles = read_dir(sys.argv[1])
#     print(pdbfiles)
    # rdd = spark.sparkContext.parallelize(pdbfiles)
    # rdd.map(lambda x: pipeline(x[0], x[1], x[2])).collect()
    # p = multiprocessing.Pool(1)
    # p.starmap(pipeline, pdbfiles[:10])

        