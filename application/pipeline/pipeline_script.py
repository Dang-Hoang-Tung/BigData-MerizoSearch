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

def run_merizo_search(input_file_path: str, input_file_id: str):
    """
    Runs the merizo domain predictor to produce domains
    """
    cmd = ['python3',
           '/home/almalinux/merizo_search/merizo_search/merizo.py',
           'easy-search',
           input_file_path,
           '/home/almalinux/cath_foldclassdb/cath-4.3-foldclassdb',
           input_file_id,
           'tmp',
           '--iterate',
           '--output_headers',
           '-d',
           'cpu',
           '--threads',
           '1'
           ]
    run_command(cmd)

def pipeline(input_file_id: str, directory: str):
    input_file_path = os.path.join(directory, input_file_id)

    # STEP 1 - Merizo search
    print(f"STEP 1: RUNNING MERIZO -> {input_file_path} - {input_file_id}")
    run_merizo_search(input_file_path, input_file_id)

    search_file_id = f"{input_file_id}_search.tsv"
    search_file_path = os.path.join(directory, search_file_id)

    # STEP 2 - Results parser
    if (os.path.exists(search_file_path)):
        print(f'STEP 2: RUNNING PARSER -> {input_file_id} - {search_file_path}')
        parsed_file_id = run_results_parser(input_file_id, search_file_path)
        return parsed_file_id
    else:
        print(f"Search file not found: {search_file_path}")
        return None
