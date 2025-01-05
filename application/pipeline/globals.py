"""
Global variables and types for the Spark application
"""

from dataclasses import dataclass

@dataclass
class JobInputs:
    """
    All the inputs required to run a full analysis job.
    """
    organism: str
    dataset: str
    hdfs_dir: str
    summary_output_path: str
    means_output_path: str

class AnalysisResults:
    """
    Represents the results of a distributed task (invoking the Merizo Search pipeline).
    Dynamically add {cath_code: count} results.
    """
    MEAN_PLDDT_KEY = "mean_plddt_list" # IMPORTANT: KEEP IN SYNC
    
    def __init__(self):
        self.mean_plddt_list = []

@dataclass
class PlddtMeans:
    """
    Represents the mean and standard deviation of the plddt values for an organism.
    """
    organism: str
    mean: float
    stdev: float

## --- Driver variables (spark_job.py) --- ##

APPLICATION_NAME = "Merizo Search Pipeline"
MIN_PARTITIONS = 22

TEST_JOB_INPUTS = JobInputs(
    organism="test",
    dataset="test",
    hdfs_dir="/test",
    summary_output_path="/test_cath_summary",
    means_output_path="/test_plDDT_means"
)

ECOLI_JOB_INPUTS = JobInputs(
    organism="ecoli",
    dataset="UP000000625_83333_ECOLI_v4",
    hdfs_dir="/UP000000625_83333_ECOLI_v4",
    summary_output_path="/ecoli_cath_summary",
    means_output_path="/ecoli_plDDT_means"
)

HUMAN_JOB_INPUTS = JobInputs(
    organism="human",
    dataset="UP000005640_9606_HUMAN_v4",
    hdfs_dir="/UP000005640_9606_HUMAN_v4",
    summary_output_path="/human_cath_summary",
    means_output_path="/human_plDDT_means"
)

COMBINED_MEANS_OUTPUT_PATH = "/plDDT_means"


## --- Worker variables (merizo_adapter.py) --- ##

# Important: These variables should only be used by the pipeline adapter component.
# The pipeline must receive all necessary information as arguments. 

ADAPTER_DIR = "/home/almalinux/merizo_files"
RECORDS_FILE_NAME = "records.txt"
