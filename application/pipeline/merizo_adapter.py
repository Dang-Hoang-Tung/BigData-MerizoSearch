from typing import Literal
import os
import time
from pipeline_script import pipeline

ADAPTER_DIR = "/home/almalinux/merizo_files"
HUMAN_DIR = "/home/almalinux/UP000005640_9606_HUMAN_v4"
ECOLI_DIR = "/home/almalinux/UP000000625_83333_ECOLI_v4"
TEST_DIR = "/home/almalinux/test"

directory_map = {
    "human": HUMAN_DIR,
    "ecoli": ECOLI_DIR,
    "test": TEST_DIR
}

def write_file_to_adapter_dir(file_name, file_content, dataset: Literal["human", "ecoli", "test"]):
    # Ensure the directory exists
    os.makedirs(directory_map[dataset], exist_ok=True)
    # Construct the full file path
    file_path = os.path.join(directory_map[dataset], file_name)
    
    # Write the file contents
    with open(file_path, 'w') as f:
        f.write(file_content)

    os.chmod(file_path, 755)

    return file_path

def run_merizo(file_name, file_content, dataset: Literal["human", "ecoli"]):
    write_file_to_adapter_dir(file_name, file_content, dataset)

    time.sleep(2)
