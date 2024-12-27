# Overview

This repository contains the solution to the coursework for module COMP0235 Engineering for Data Analysis 1 (2024/2025).

## Directory structure

```
project-root
├── infrastructure
│   └── terraform   # Terraform code for infrastructure
├── configuration
│   ├── ansible     # Ansible playbooks and roles
│   └── templates   # Jinja2 templates
├── application
│   ├── python      # Pipeline scripts
│   └── tests       # Tests
```

## Cluster specifications

These specifications adhere to the constraints of the given task. However, the code is flexible to modify the cluster as requirements change.

| _Type_    | _Purpose_          | _Machine IDs_                             | _Number_ | _Cores_ | _RAM_     | _HDD1_   | _HDD2_    |
| --------- | ------------------ | ----------------------------------------- | -------- | ------- | --------- | -------- | --------- |
| Host      | Cluster head       | mgmtnode                                  | 1        | 2       | 4GB       | 10GB     | -         |
| Worker    | Pipeline execution | workernode1<br>workernode2<br>workernode3 | 3        | 4       | 32GB      | 25GB     | -         |
| Storage   | Long-term storage  | storagenode                               | 1        | 4       | 8GB       | 10GB     | 200gb     |
| **Total** | **-**              | **-**                                     | **5**    | **18**  | **108GB** | **95GB** | **200GB** |

# Instructions

All commands should be run from the _project root directory_. Please use `screen` or `tmux` to persist the session as the scripts can take a long time to execute.

## Provisioning infrastructure

**Command**:

`(cd infrastructure/terraform && terraform init && terraform apply -auto-approve)`

Individually:

```bash
cd infrastructure/terraform
terraform init
terraform apply -auto-approve
cd ../..
```

## Configuring machines

### Initial state

> Command: ``

### Pipeline setup

> Command: ``

## Running the pipeline

### Application

> Command: ``

### Tests

> Command: ``
