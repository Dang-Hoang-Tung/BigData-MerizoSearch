import os
from pipeline.pipeline_script import pipeline

ADAPTER_DIR = "/home/almalinux/merizo_files"

def write_file_to_adapter_dir(file_id: str, file_content: str, directory: str):
    file_path = os.path.join(directory, file_id)
    with open(file_path, 'w') as f:
        f.write(file_content)
    # os.chmod(file_path, 777)
    return file_path

def run_merizo(file_path: str, file_id: str, directory: str):
    pipeline(file_path, file_id, directory)

def merizo_adapter(file_id: str, file_content: str, dataset: str):
    directory = os.path.join(ADAPTER_DIR, dataset)
    os.makedirs(directory, mode=0o777, exist_ok=True)

    write_file_to_adapter_dir(file_id, file_content, directory)
    run_merizo(file_id, file_content, directory)
