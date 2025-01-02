import os
from pipeline.pipeline_script import pipeline as run_merizo

ADAPTER_DIR = "/home/almalinux/merizo_files"

def merizo_adapter(file_id: str, file_content: str, dataset: str):
    # Create the directory if it does not exist
    directory = os.path.join(ADAPTER_DIR, dataset)
    os.makedirs(directory, mode=0o777, exist_ok=True)

    # Write the file to disk
    file_path = os.path.join(directory, file_id)
    with open(file_path, 'w') as f:
        f.write(file_content)

    # Run the pipeline to read from disk and process .pdb file
    run_merizo(file_path)
