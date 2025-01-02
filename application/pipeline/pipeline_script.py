from subprocess import Popen, PIPE
import os
from pipeline.results_parser import run_results_parser

"""
usage: python pipeline_script.py [INPUT DIR] [OUTPUT DIR]
approx 5seconds per analysis
"""

def run_command(msg: str, cmd: list):
    """
    Runs the subshell command and prints the output.
    Ensuring we have the correct environment variables.
    """
    print(f'{msg} -> {" ".join(cmd)}')
    env = os.environ.copy()  # Copy the current environment
    env['PWD'] = os.getcwd()  # Explicitly set PWD
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=os.getcwd(), env=env)
    out, err = p.communicate()
    print(out.decode("utf-8"))
    print(err.decode("utf-8"))

# def get_results_parser_path():
#     """
#     Returns the path to the results_parser.py script, which should be adjacent to this script.
#     """
#     script_directory = os.path.dirname(os.path.abspath(__file__))
#     return os.path.join(script_directory, 'results_parser.py')

def run_parser(file_id: str, output_dir: str):
    """
    Run the results_parser.py over the hhr file to produce the output summary
    """
    search_result_path = os.path.join(output_dir, f'{file_id}_search.tsv')
    # results_parser_path = get_results_parser_path()
    # cmd = ['python', results_parser_path, output_dir, search_result_file]
    # run_command("STEP 2: RUNNING PARSER", cmd)
    print(f'STEP 2: RUNNING PARSER -> {file_id} - {search_result_path}')
    run_results_parser(file_id, search_result_path)

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
           '2'
           ]
    run_command('STEP 1: RUNNING MERIZO', cmd)

def pipeline(file_path: str, file_id: str, output_dir: str):
    # STEP 1
    run_merizo_search(file_path, file_id)
    # STEP 2
    run_parser(file_id, output_dir)
