#!/usr/bin/env python3

import json
import subprocess
import argparse
import os
import sys

# Terraform output variables - keep in sync!
TERRAFORM_DIRECTORY = "infrastructure"
TERRAFORM_MGMT_IPS_KEY = "mgmt_vm_ips"
TERRAFORM_STORAGE_IPS_KEY = "storage_vm_ips"
TERRAFORM_WORKER_IPS_KEY = "worker_vm_ips"

# Ansible groups
ANSIBLE_MGMT_GROUP = "mgmtgroup"
ANSIBLE_STORAGE_GROUP = "storagegroup"
ANSIBLE_WORKER_GROUP = "workergroup"
ANSIBLE_ALL_GROUPS = [ANSIBLE_MGMT_GROUP, ANSIBLE_STORAGE_GROUP, ANSIBLE_WORKER_GROUP]

# Ansible hosts
ANSIBLE_MGMT_NODE = "mgmtnode"
ANSIBLE_STORAGE_NODE = "storagenode"
ANSIBLE_WORKER_NODE_PREFIX = "workernode"

def get_terraform_output(ips_key):
    working_dir = os.getcwd()
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        os.chdir(f"{current_script_dir}/../{TERRAFORM_DIRECTORY}")
        result = subprocess.run(['terraform', 'output', '--json', ips_key], capture_output=True, encoding='UTF-8')
        terraform_output = json.loads(result.stdout)
        return terraform_output
    except subprocess.CalledProcessError as e:
        print(f"Error executing Terraform: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        os.chdir(working_dir)

# def get_ips(ips_key):
#     command = f"terraform output --json {ips_key}".split()
#     output = subprocess.run(command, capture_output=True, encoding='UTF-8').stdout
#     return json.loads(output)

def generate_inventory():
    mgmt_ips = get_terraform_output(TERRAFORM_MGMT_IPS_KEY)
    storage_ips = get_terraform_output(TERRAFORM_STORAGE_IPS_KEY)
    worker_ips = get_terraform_output(TERRAFORM_WORKER_IPS_KEY)

    host_vars = {
        ANSIBLE_MGMT_NODE: { "ansible_host": mgmt_ips[0] },
        ANSIBLE_STORAGE_NODE: { "ansible_host": storage_ips[0] },
    }
    
    worker_nodes = []
    for i, worker_ip in enumerate(worker_ips):
        name = f"{ANSIBLE_WORKER_NODE_PREFIX}{i + 1}"
        host_vars[name] = { "ansible_host": worker_ip }
        worker_nodes.append(name)

    _jd = {
        # Metadata
        "_meta": { "hostvars": host_vars},
        "all": { "children": ANSIBLE_ALL_GROUPS },
        "ungrouped": { "hosts": [] },

        # Groups
        ANSIBLE_MGMT_GROUP: { "hosts": [ANSIBLE_MGMT_NODE] },
        ANSIBLE_STORAGE_GROUP: { "hosts": [ANSIBLE_STORAGE_NODE] },
        ANSIBLE_WORKER_GROUP: { "hosts": worker_nodes },
    }

    jd = json.dumps(_jd, indent=4)
    return jd

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description = "Generate a cluster inventory from Terraform.",
        prog = __file__
    )

    mo = ap.add_mutually_exclusive_group()
    mo.add_argument("--list",action="store", nargs="*", default="dummy", help="Show JSON of all managed hosts")
    mo.add_argument("--host",action="store", help="Display vars related to the host")
    mo.add_argument("--test",action="store_true", help="Run test and print")

    args = ap.parse_args()

    if args.host:
        print(json.dumps({}))
    elif len(args.list) >= 0:
        jd = generate_inventory()
        print(jd)
    else:
        raise ValueError("Expecting either --host $HOSTNAME or --list")
