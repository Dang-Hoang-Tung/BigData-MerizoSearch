import csv
import json
from collections import defaultdict
import statistics
import os

def write_parsed_file(input_file_id: str, search_file_id: str, plDDT_values: list, cath_ids: dict):
    parsed_file_id = f"{input_file_id}.parsed"
    with open(f"{input_file_id}.parsed", "w", encoding="utf-8") as fhOut:
        if len(plDDT_values) > 0:
            fhOut.write(f"#{search_file_id} Results. mean plddt: {statistics.mean(plDDT_values)}\n")
        else:
            fhOut.write(f"#{search_file_id} Results. mean plddt: 0\n")

        fhOut.write("cath_id,count\n")

        for cath, v in cath_ids.items():
            fhOut.write(f"{cath},{v}\n")

    return parsed_file_id

def run_results_parser(input_file_id: str, search_file_path: str):
    cath_ids = defaultdict(int)
    plDDT_values = []

    with open(search_file_path, "r") as fhIn:
        next(fhIn)
        msreader = csv.reader(fhIn, delimiter='\t',) 
        tot_entries = 0
        for i, row in enumerate(msreader):
            tot_entries = i+1
            plDDT_values.append(float(row[3]))
            meta = row[15]
            data = json.loads(meta)
            cath_ids[data["cath"]] += 1

        search_file_id = os.path.basename(search_file_path)
        parsed_file_id = write_parsed_file(input_file_id, search_file_id, plDDT_values, cath_ids)

        return parsed_file_id
