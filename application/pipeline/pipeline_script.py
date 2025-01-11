from subprocess import Popen, PIPE
import os
from pipeline.results_parser import run_results_parser
from typing import Optional

def run_command(cmd: list) -> None:
    """
    Runs the subshell command and prints the output.
    Ensuring we have the correct environment variables.
    """
    env = os.environ.copy()  # Copy the current environment
    env['PWD'] = os.getcwd()  # Explicitly set PWD
    env["MPLCONFIGDIR"] = "/tmp/matplotlib_config"
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=os.getcwd(), env=env)
    out, err = p.communicate()
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))

def run_merizo_search(input_file_id: str) -> None:
    """
    Runs the merizo domain predictor to produce domains
    """
    cmd = ['python3',
           '/home/almalinux/merizo_search/merizo_search/merizo.py',
           'easy-search',
           input_file_id, # Path to file. Using relative path.
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

def pipeline(input_file_id: str) -> Optional[str]:
    """
    Executes the Merizo Search pipeline for the input file.

    Returns:
        The parsed file ID if it exists, otherwise None.
    """
    # STEP 1 - Merizo search
    print(f"STEP 1: RUNNING MERIZO - {input_file_id}")
    run_merizo_search(input_file_id)

    search_file_id = f"{input_file_id}_search.tsv"

    # STEP 2 - Results parser
    if (os.path.exists(search_file_id)):
        print(f'STEP 2: RUNNING PARSER -> {input_file_id} - {search_file_id}')
        parsed_file_id = run_results_parser(input_file_id, search_file_id)
        return parsed_file_id
    else:
        print(f"Search file not found: {input_file_id} - {search_file_id}")
        return None
