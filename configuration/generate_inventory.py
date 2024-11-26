#!/usr/bin/env python3

import json
import subprocess
import argparse

# Variables to be retrieved from Terraform output - keep in sync!
MGMT_IPS_KEY = "mgmt_vm_ips"
STORAGE_IPS_KEY = "storage_vm_ips"
WORKER_IPS_KEY = "worker_vm_ips"

def run(command):
    return subprocess.run(command, capture_output=True, encoding='UTF-8')

def get_ips_from_terraform_output(ips_key):
    get_ips_command = f"terraform output --json {ips_key}".split()
    return json.loads(run(get_ips_command).stdout)

def generate_inventory(get_ips):
    mgmt_ips = get_ips(MGMT_IPS_KEY)
    storage_ips = get_ips(STORAGE_IPS_KEY)
    worker_ips = get_ips(WORKER_IPS_KEY)

    host_vars = {
        "mgmt_node": { "ansible_host": mgmt_ips[0] },
        "storage_node": { "ansible_host": storage_ips[0] },
    }
    
    worker_nodes = []
    for i, worker_ip in enumerate(worker_ips):
        name = f"worker_node_{i}"
        host_vars[name] = { "ansible_host": worker_ip }
        worker_nodes.append(name)

    _jd = {
        # Metadata
        "_meta": { "hostvars": host_vars},
        "all": { "children": ["mgmt_group", "storage_group", "worker_group"] },
        "ungrouped": { "hosts": [] },

        # Groups
        "mgmt_group": { "hosts": ["mgmt_node"] },
        "storage_group": { "hosts": ["storage_node"] },
        "worker_group": { "hosts": worker_nodes },
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
        jd = generate_inventory(get_ips_from_terraform_output)
        print(jd)
    else:
        raise ValueError("Expecting either --host $HOSTNAME or --list")
