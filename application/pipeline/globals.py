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

@dataclass
class AnalysisResults(dict):
    """
    Dict-like class for type safety (bunch of methods that just implement the dict functionality).
    Represents the results of a distributed task (invoking the Merizo Search pipeline).
    Dynamically add {cath_code: count} results.
    """
    MEAN_PLDDT_KEY = "mean_plddt_list" # IMPORTANT: KEEP IN SYNC
    mean_plddt_list: list = None # IMPORTANT: KEEP IN SYNC
    
    def __post_init__(self):
        # Initialize the list to an empty list if not provided
        if self.mean_plddt_list is None:
            self.mean_plddt_list = []

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))

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
