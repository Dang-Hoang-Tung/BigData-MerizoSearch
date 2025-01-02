import os
import time
from pipeline.pipeline_script import pipeline

ADAPTER_DIR = "/home/almalinux/merizo_files"

def write_file_to_adapter_dir(file_name: str, file_content: str, directory: str):
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as f:
        f.write(file_content)
    # os.chmod(file_path, 777)
    return file_path

def run_merizo(file_path: str, file_id: str, dataset: str):
    pipeline(file_path, file_id, dataset)

def merizo_adapter(file_name: str, file_content: str, dataset: str):
    directory = os.path.join(ADAPTER_DIR, dataset)
    os.makedirs(directory, mode=0o777, exist_ok=True)

    write_file_to_adapter_dir(file_name, file_content, directory)

    # time.sleep(5)
