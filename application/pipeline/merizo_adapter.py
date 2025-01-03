import os
import re
from pipeline.pipeline_script import pipeline as run_merizo

ADAPTER_DIR = "/home/almalinux/merizo_files"

def read_parsed_file_to_dict(file_id: str, file_path: str, file_id_key: str, mean_plddt_key: str):
    data_dict = {}
    with open(file_path, mode='r') as file:
        lines = file.readlines()
        for line in lines:
            # Parse comment line for mean plddt
            if line.startswith('#'):
                match = re.search(r'mean plddt:\s*([0-9.]+)', line)
                data_dict[file_id_key] = file_id
                data_dict[mean_plddt_key] = float(match.group(1))
            # Skip the header line
            elif line.startswith('cath_id,count'):
                continue
            # Read the subsequent lines for cath_id and count
            else:
                [cath_id, count] = line.strip().split(',')
                data_dict[cath_id] = int(count)
    return data_dict

def merizo_adapter(file_id: str, file_content: str, dataset: str, file_id_key: str, mean_plddt_key: str):
    # Create the directory if it does not exist
    directory = os.path.join(ADAPTER_DIR, dataset)
    os.makedirs(directory, mode=0o777, exist_ok=True)

    # Write the file to disk
    file_path = os.path.join(directory, file_id)
    with open(file_path, 'w') as f:
        f.write(file_content)

    # Run the pipeline to read from disk and process .pdb file
    parsed_file_id = run_merizo(file_id, directory)

    if parsed_file_id is None:
        return {}
    else:
        # Read the results from the parser
        parsed_file_path = os.path.join(directory, parsed_file_id)
        return read_parsed_file_to_dict(file_id, parsed_file_path, file_id_key, mean_plddt_key)
