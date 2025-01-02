import sys
import csv
import json
from collections import defaultdict
import statistics
import os
# fhOut = open(sys.argv[1]."summmary", "w")
# fhOut.write('ID,domain_count\n')

def write_parsed_file(file_id: str, search_result_file_name: str, plDDT_values: list, cath_ids: dict):
    with open(f"{file_id}.parsed", "w", encoding="utf-8") as fhOut:
        if len(plDDT_values) > 0:
            fhOut.write(f"#{search_result_file_name} Results. mean plddt: {statistics.mean(plDDT_values)}\n")
        else:
            fhOut.write(f"#{search_result_file_name} Results. mean plddt: 0\n")

        fhOut.write("cath_id,count\n")

        for cath, v in cath_ids.items():
            fhOut.write(f"{cath},{v}\n")

def run_results_parser(file_id: str, search_result_path: str):
    cath_ids = defaultdict(int)
    plDDT_values = []

    with open(search_result_path, "r") as fhIn:
        next(fhIn)
        msreader = csv.reader(fhIn, delimiter='\t',) 
        tot_entries = 0
        for i, row in enumerate(msreader):
            tot_entries = i+1
            plDDT_values.append(float(row[3]))
            meta = row[15]
            data = json.loads(meta)
            cath_ids[data["cath"]] += 1

        search_result_file_name = os.path.basename(search_result_path)
        write_parsed_file(file_id, search_result_file_name, plDDT_values, cath_ids)
