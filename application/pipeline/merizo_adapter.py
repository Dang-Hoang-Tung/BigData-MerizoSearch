from global_vars import *
import os
import re
from pipeline.pipeline_script import pipeline as run_merizo

def read_parsed_file_to_dict(parsed_file_path: str):
    results_dict = AnalysisResults()
    with open(parsed_file_path, mode='r') as file:
        lines = file.readlines()
        for line in lines:
            # Parse comment line for mean plddt
            if line.startswith('#'):
                match = re.search(r'mean plddt:\s*([0-9.]+)', line)
                if match:
                    results_dict.mean_plddt_list = [float(match.group(1))]
            # Skip the header line
            elif line.startswith('cath_id,count'):
                continue
            # Read the subsequent lines for cath_id and count
            else:
                [cath_id, count] = line.strip().split(',')
                results_dict[cath_id] = int(count)
    return results_dict

def merizo_adapter(input_file_id: str, input_file_content: str, dataset: str):
    # Create the directory if it does not exist
    directory = os.path.join(ADAPTER_DIR, dataset)
    os.makedirs(directory, mode=0o777, exist_ok=True)

    # Write the file to disk
    input_file_path = os.path.join(directory, input_file_id)
    with open(input_file_path, 'w') as f:
        f.write(input_file_content)

    # Ensure our entire pipeline runs in the correct directory
    os.chdir(directory)
    # Run the pipeline to read from disk and process .pdb file
    parsed_file_id = run_merizo(input_file_id, directory)

    # Record the input and parsed file ids
    records_file_path = os.path.join(directory, RECORDS_FILE_NAME)
    with open(records_file_path, 'a') as records_file:
        records_file.write(f"{input_file_id} - {str(parsed_file_id)}\n")

    # Remove the input file on disk after processing and recording
    os.remove(input_file_path)

    if parsed_file_id is None:
        return {}

    # Read and return the parsed results
    parsed_file_path = os.path.join(directory, parsed_file_id)
    return read_parsed_file_to_dict(parsed_file_path)
