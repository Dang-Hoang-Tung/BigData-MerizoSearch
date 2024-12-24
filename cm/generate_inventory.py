#!/usr/bin/env python3

import json
import subprocess
import argparse

# Variables to retrieve Terraform output - keep in sync!
TERRAFORM_RELATIVE_PATH = "../iac"
MGMT_IPS_KEY = "mgmt_vm_ips"
STORAGE_IPS_KEY = "storage_vm_ips"
WORKER_IPS_KEY = "worker_vm_ips"

def get_terraform_output(output_key=None):
    """
    Get Terraform output from a specified directory.

    Args:
        output_key (str): Specific key to fetch from the outputs. If None, return all outputs.

    Returns:
        dict or str: Entire output as a dictionary if output_key is None, otherwise the value of the specific key.
    """
    try:
        # Run the `terraform output -json` command
        result = subprocess.run(
            ["terraform", "output", "-json"],
            cwd=TERRAFORM_RELATIVE_PATH,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Parse the JSON output
        outputs = json.loads(result.stdout)

        if output_key:
            # Return the specific output value if a key is provided
            return outputs.get(output_key, {}).get("value")
        else:
            # Return all outputs as a dictionary
            return {key: value["value"] for key, value in outputs.items()}

    except subprocess.CalledProcessError as e:
        print(f"Error running Terraform: {e.stderr}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def run(command):
    return subprocess.run(command, capture_output=True, encoding='UTF-8')

def get_ips(ips_key):
    bash_command = f"(cd {TERRAFORM_RELATIVE_PATH} && terraform output --json {ips_key})".split()
    return json.loads(run(bash_command).stdout)

def generate_inventory():
    mgmt_ips = get_terraform_output(MGMT_IPS_KEY)
    storage_ips = get_terraform_output(STORAGE_IPS_KEY)
    worker_ips = get_terraform_output(WORKER_IPS_KEY)

    host_vars = {
        "mgmtnode": { "ansible_host": mgmt_ips[0] },
        "storagenode": { "ansible_host": storage_ips[0] },
    }
    
    worker_nodes = []
    for i, worker_ip in enumerate(worker_ips):
        name = f"workernode{i + 1}"
        host_vars[name] = { "ansible_host": worker_ip }
        worker_nodes.append(name)

    _jd = {
        # Metadata
        "_meta": { "hostvars": host_vars},
        "all": { "children": ["mgmtgroup", "storagegroup", "workergroup"] },
        "ungrouped": { "hosts": [] },

        # Groups
        "mgmtgroup": { "hosts": ["mgmtnode"] },
        "storagegroup": { "hosts": ["storagenode"] },
        "workergroup": { "hosts": worker_nodes },
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
