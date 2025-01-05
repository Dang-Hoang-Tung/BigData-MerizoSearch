"""
Config variables for the Spark application
"""

class JobInputs:
    """
    All the inputs required to run a full analysis job.
    """
    def __init__(self, organism, dataset, hdfs_dir, summary_output_path, means_output_path):
        self.organism = organism
        self.dataset = dataset
        self.hdfs_dir = hdfs_dir
        self.summary_output_path = summary_output_path
        self.means_output_path = means_output_path

class AnalysisResults:
    """
    Represents the results of a distributed task (invoking the Merizo Search pipeline).
    Dynamically add {cath_code: count} results.
    """
    MEAN_PLDDT_KEY = "mean_plddt_list" # IMPORTANT: KEEP IN SYNC

    def __init__(self):
        self.mean_plddt_list = [] # IMPORTANT: KEEP IN SYNC


## --- Driver variables (spark_job.py) --- ##

APPLICATION_NAME = "Merizo Search Pipeline"

TEST_DATASET = "test"
TEST_DATASET_HDFS_DIR = f'/{TEST_DATASET}'
TEST_SUMMARY_OUTPUT_PATH = "/test_cath_summary.csv"
TEST_MEANS_OUTPUT_PATH = "/test_plDDT_means.csv"
TEST_ORGANISM = "test"
TEST_JOB_INPUTS = JobInputs(TEST_ORGANISM, TEST_DATASET, TEST_DATASET_HDFS_DIR, TEST_SUMMARY_OUTPUT_PATH, TEST_MEANS_OUTPUT_PATH)

ECOLI_DATASET = "UP000000625_83333_ECOLI_v4"
ECOLI_DATASET_HDFS_DIR = f"/{ECOLI_DATASET}"
ECOLI_SUMMARY_OUTPUT_PATH = "/ecoli_cath_summary.csv"
ECOLI_MEANS_OUTPUT_PATH = "/ecoli_plDDT_means.csv"
ECOLI_ORGANISM = "ecoli"
ECOLI_JOB_INPUTS = JobInputs(ECOLI_ORGANISM, ECOLI_DATASET, ECOLI_DATASET_HDFS_DIR, ECOLI_SUMMARY_OUTPUT_PATH, ECOLI_MEANS_OUTPUT_PATH)

HUMAN_DATASET = "UP000005640_9606_HUMAN_v4"
HUMAN_DATASET_HDFS_DIR = f"/{HUMAN_DATASET}"
HUMAN_SUMMARY_OUTPUT_PATH = "/human_cath_summary.csv"
HUMAN_MEANS_OUTPUT_PATH = "/human_plDDT_means.csv"
HUMAN_ORGANISM = "human"
HUMAN_JOB_INPUTS = JobInputs(HUMAN_ORGANISM, HUMAN_DATASET, HUMAN_DATASET_HDFS_DIR, HUMAN_SUMMARY_OUTPUT_PATH, HUMAN_MEANS_OUTPUT_PATH)

COMBINED_MEANS_OUTPUT_PATH = "/plDDT_means.csv"


## --- Worker variables (merizo_adapter.py) --- ##

# Important: These variables should only be used by the pipeline adapter component.
# The pipeline must receive all necessary information as arguments. 

ADAPTER_DIR = "/home/almalinux/merizo_files"
RECORDS_FILE_NAME = "records.txt"
