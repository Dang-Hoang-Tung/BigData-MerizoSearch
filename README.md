# Overview

This repository contains the solution to the coursework for module COMP0235 Engineering for Data Analysis 1 (2024/2025).

## Directory Structure

```
project
│
├── infrastructure      # (Terraform) Provision infrastructure
│   └── modules         # - Reusable submodules
│
├── configuration       # (Ansible) Configure machines and set up pipeline
│   ├── common          # - Environment initial setup (all nodes)
│   ├── storage         # - Mount second disk and set up Minio server (storage node)
│   ├── monitoring      # - Set up Prometheus and Grafana (mgmt node)
│   ├── hadoop-spark    # - Installing Hadoop and Spark (mgmt, worker nodes)
│   ├── pipeline        # - Distributing the data and preparing the pipeline (all nodes)
│   └── serve-results   # - Collect the data and serve on S3 server (storage, worker nodes)
│
├── application         # (PySpark) Run the distributed analysis
│   ├── example_files   # - Provided example files from the lovely researchers (can ignore)
│   └── pipeline        # - Code to run the Spark job, deploying the pipeline
```

In this project, folders use `kebab-case` and files use `snake_case`.

## Cluster Specifications

These are the default specifications. They adhere to the constraints of the provided requirements. However, the infrastructure code is very flexible, new changes in specifications can simply be added to `config.tfvars` file. Then, the file can be passed into `terraform apply`.

| _Assigned IDs_                            | _Type_  | _Purpose_          | _Number_ | _Cores_ | _RAM_     | _HDD1_   | _HDD2_    |
| ----------------------------------------- | ------- | ------------------ | -------- | ------- | --------- | -------- | --------- |
| mgmtnode                                  | Host    | Cluster head       | 1        | 2       | 4GB       | 10GB     | -         |
| workernode1<br>workernode2<br>workernode3 | Worker  | Pipeline execution | 3        | 4       | 32GB      | 25GB     | -         |
| storagenode                               | Storage | Long-term storage  | 1        | 4       | 8GB       | 10GB     | 200GB     |
| **Total**                                 | **-**   | **-**              | **5**    | **18**  | **108GB** | **95GB** | **200GB** |

### Pre-configured Cluster

**S3 storage for outputs**

This cluster has been pre-configured to run the pipeline. It is serving the required outputs at `s3-6f80ac3cd9783ccf.comp0235.condenser.arc.ucl.ac.uk/merizo-outputs`.

**VM IDs and IPs**

The IDs and IPs are provided below as per terraform outputs. The `lecturer_key.pub` has been added to `authorized_keys` for access to all machines:

```
mgmt_vm_ids = [
"ucabhtd-comp0235-ns/merizo-search-mgmt-6f80ac3cd9783ccf",
]
mgmt_vm_ips = [
"10.134.12.127",
]
storage_vm_ids = [
"ucabhtd-comp0235-ns/merizo-search-storage-6f80ac3cd9783ccf",
]
storage_vm_ips = [
"10.134.12.132",
]
worker_vm_ids = [
"ucabhtd-comp0235-ns/merizo-search-worker-1-6f80ac3cd9783ccf",
"ucabhtd-comp0235-ns/merizo-search-worker-2-6f80ac3cd9783ccf",
"ucabhtd-comp0235-ns/merizo-search-worker-3-6f80ac3cd9783ccf",
]
worker_vm_ips = [
"10.134.12.86",
"10.134.12.91",
"10.134.12.111",
]
```

**Service hostnames**

Many services are running as part of the pipeline. The hostnames below can be used to access each elements during execution through the Web UI. Simply append `.comp0235.condenser.arc.ucl.ac.uk` to any hostname. For node_exporter, append `-1 or -2 or -3` to the hostname prior to the rest of the URL, depending on the worker node (e.g. "nodeexporter-6f80ac3cd9783ccf-1").

```
hostnames = {
"grafana" = "grafana-6f80ac3cd9783ccf"
"hdfs" = "hdfs-6f80ac3cd9783ccf"
"minio_console" = "cons-6f80ac3cd9783ccf"
"minio_s3" = "s3-6f80ac3cd9783ccf"
"node_exporter" = "nodeexporter-6f80ac3cd9783ccf"
"prometheus" = "prometheus-6f80ac3cd9783ccf"
"yarn" = "yarn-6f80ac3cd9783ccf"
}
```

---

# Instructions (to execute and test)

**Important!**

Conditions to ensure smooth execution:

- Please use `tmux` or `screen` to persist the session as the scripts can take a long time to execute.
- The Ansible scripts assume that the running machine automatically accepts new hosts. Please check your machine's `~/.ssh/config` is configured with `StrictHostKeyChecking accept-new` for all hosts.
- The terraform state of the cluster should be accessible to the `configuration/inventory.py` file for Ansible to run. Simply ensure `terraform init` has been executed prior (more details below).
- All commands provided assume the current directory is the project's root.

About the configuration pipeline:

- All configuration steps are idempotent and can be run independently (provided the prior steps have been run at least once).
- Each set of instructions will refer to the entire configuration process together, but please feel free to replace **index.yaml** (the parent script) with any of these individual steps below:
  - **common/main.yaml**: Environment initial setup (all nodes)
  - **storage/main.yaml**: Mount second disk and set up Minio server (storage node)
  - **monitoring/main.yaml**: Set up Prometheus and Grafana (mgmt node)
  - **hadoop-spark/main.yaml**: Install Hadoop and Spark (mgmt, worker nodes)
  - **pipeline/main.yaml**: Distribute the data, code and run the analysis pipeline (all nodes)
  - **serve-results/main.yaml**: Collect the data and serve on S3 server (storage, worker nodes)

## Testing the pre-configured cluster

**Option 1. Using external machine**

- Clone this repo to your machine, ensure the conditions mentioned above are met.
- Initialise infrastructure
  ```
  (cd infrastructure && terraform init)
  ```
- Run whole pipeline
  ```
  (cd configuration && ansible-playbook -i inventory.py index.yaml)
  ```

**Option 2. Hop into the mgmtnode machine**

- Use the IP address provided above to hop into mgmtnode.
- Here you can test the Spark execution
  ```
  spark-submit --deploy-mode cluster --master yarn application/pipeline/spark_job.py
  ```
- Spark will deploy the pipeline to worker nodes, which will run the Merizo Search application.
- The output .tsv and .parsed files are produced on the worker nodes, they are uploaded and served separately to the Spark application. (Ansible script is serve-results/main.yaml)
- The summary outputs are returned to the Spark driver and uploaded to HDFS, these can be inspected immediately when the job finishes on the Web UI using the HDFS hostname (see above).

## Testing a fresh cluster

- Clone this repo to your machine, ensure the conditions mentioned above are met.
- Initialise and provision the infrastructure
  ```
  (cd infrastructure && terraform init && terraform apply -auto-approve)
  ```
- Run whole pipeline
  ```
  (cd configuration && ansible-playbook -i inventory.py index.yaml)
  ```
