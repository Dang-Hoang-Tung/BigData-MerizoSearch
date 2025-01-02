import os
import time
from pipeline_script import pipeline

ADAPTER_DIR = "/home/almalinux/merizo_files"

def write_file_to_adapter_dir(file_name, file_content):
    # Ensure the directory exists
    os.makedirs(ADAPTER_DIR, exist_ok=True)
    # Construct the full file path
    file_path = os.path.join(ADAPTER_DIR, file_name)
    
    # Write the file contents
    with open(file_path, 'w') as f:
        f.write(file_content)

    return file_path

def run_merizo(file_name, file_content):
    write_file_to_adapter_dir(file_name, file_content)
    
    time.sleep(2)
