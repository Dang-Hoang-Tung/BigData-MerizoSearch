from subprocess import Popen, PIPE
import os
from pipeline.results_parser import run_results_parser

"""
usage: python pipeline_script.py [INPUT DIR] [OUTPUT DIR]
approx 5seconds per analysis
"""

def run_command(cmd: list):
    """
    Runs the subshell command and prints the output.
    Ensuring we have the correct environment variables.
    """
    env = os.environ.copy()  # Copy the current environment
    env['PWD'] = os.getcwd()  # Explicitly set PWD
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=os.getcwd(), env=env)
    out, err = p.communicate()
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))

def run_merizo_search(file_path: str, file_id: str):
    """
    Runs the merizo domain predictor to produce domains
    """
    cmd = ['python3',
           '/home/almalinux/merizo_search/merizo_search/merizo.py',
           'easy-search',
           file_path,
           '/home/almalinux/cath_foldclassdb/cath-4.3-foldclassdb',
           file_id,
           'tmp',
           '--iterate',
           '--output_headers',
           '-d',
           'cpu',
           '--threads',
           '1'
           ]
    run_command(cmd)

def pipeline(file_id: str, directory: str):
    file_path = os.path.join(directory, file_id)

    # STEP 1 - Merizo search
    print(f"STEP 1: RUNNING MERIZO -> {file_path} - {file_id}")
    run_merizo_search(file_path, file_id)

    # STEP 2 - Results parser
    search_file_id = f"{file_id}_search.tsv"
    search_result_path = os.path.join(directory, search_file_id)
    print(f'STEP 2: RUNNING PARSER -> {file_id} - {search_result_path}')
    if (os.path.exists(search_result_path)):
        parsed_file_id = run_results_parser(file_id, search_result_path)
        return parsed_file_id
    else:
        print(f"Search result file not found: {search_result_path}")
        return None
