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

class CathCodeTally(dict):
    """
    Contains the {cath_code: count} results of a Merizo Search run on a single PDB file.
    """
    def __init__(self):
        # Initialize the dictionary, should always start empty
        super().__init__()

    def __setitem__(self, key, value: int) -> None:
        super().__setitem__(key, value)

    def __getitem__(self, key) -> int:
        return super().__getitem__(key)

@dataclass
class Plddt:
    """
    Contains the plddt values of a Merizo Search run on a single PDB file.
    """
    size: int # Size of the population of plddt values
    mean: float # Mean of the plddt values
    variance: float # Variance of the plddt values

@dataclass
class AnalysisResults:
    """
    Contains the combined results of a distributed task (invoking the Merizo Search pipeline).
    """
    organism: str
    plddt: Plddt
    cath_code_tally: CathCodeTally

    def __init__(self, organism=None, plddt=None, cath_code_tally=None):
        self.organism = organism if organism else ""
        self.plddt = plddt if plddt else Plddt(size=0, mean=0, variance=0)
        self.cath_code_tally = cath_code_tally if cath_code_tally else CathCodeTally()

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
