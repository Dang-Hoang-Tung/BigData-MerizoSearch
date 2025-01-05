# Overview

This repository contains the solution to the coursework for module COMP0235 Engineering for Data Analysis 1 (2024/2025).

## Directory Structure

```
project
│
├── infrastructure   # (Terraform) Provision infrastructure
│   └── modules      # - Reusable infra modules
│
├── configuration    # (Ansible) Configure machines
│   ├── cluster      # - Cluster setup
│   └── pipeline     # - Data and pipeline setup
│
├── application      # (Python) Run analysis
│   ├── pipeline     # - Pipeline
│   └── aggregate    # - Results aggregation
```

In this project, folders use `kebab-case` and files use `snake_case`.

## Cluster Specifications

These are the default specifications. They adhere to the constraints of the given task.
However, the code is flexible to changes in requirements.

| _Type_    | _Purpose_          | _Machine IDs_                             | _Number_ | _Cores_ | _RAM_     | _HDD1_   | _HDD2_    |
| --------- | ------------------ | ----------------------------------------- | -------- | ------- | --------- | -------- | --------- |
| Host      | Cluster head       | mgmtnode                                  | 1        | 2       | 4GB       | 10GB     | -         |
| Worker    | Pipeline execution | workernode1<br>workernode2<br>workernode3 | 3        | 4       | 32GB      | 25GB     | -         |
| Storage   | Long-term storage  | storagenode                               | 1        | 4       | 8GB       | 10GB     | 200GB     |
| **Total** | **-**              | **-**                                     | **5**    | **18**  | **108GB** | **95GB** | **200GB** |

---

# System Requirements

python >=3.7

---

# Execution Instructions

- The commands should be run from the _project root directory_ (especially for Ansible, see below).
- Please use `screen` or `tmux` to persist the session as the scripts can take a long time to execute.

## Infrastructure Provision

> Command: `(cd terraform-infrastructure && terraform init && terraform apply -auto-approve)`

Or individually:

```bash
cd terraform-infrastructure
terraform init
terraform apply -auto-approve
cd ..
```

## Configuration Management

The Ansible inventory is generated using the [inventory.py](configuration/inventory.py) script.
This script uses a relative directory in order to reach into the [infrastructure](./infrastructure)
module and retrieve the terraform output, which is parsed into an Ansible-friendly JSON inventory.
Therefore, all Ansible scripts should be run from the _project root directory_.

### Initial State

> Command: ``

### Analysis Setup

> Command: ``

## Pipeline Execution

> Command: ``

---

# Testing

Not required for execution, just tests.

## Terraform

> Command: `(cd terraform-infrastructure && terraform fmt -check -recursive && terraform init && terraform validate)`

Or individually:

```bash
cd terraform-infrastructure
terraform fmt -check -recursive
terraform init
terraform validate
cd ..
```

## Pipeline code
