#!/usr/bin/env python

import json
import sys
from pytablewriter import MarkdownTableWriter
import toml
import requests

if len(sys.argv) != 2:
    print(
        """Usage: python 0_create_manifest.py <base_folder>
          
base_folder shoud be the local path to the folder pointed by the
FOLDER variable in the config.toml file."""
    )
    sys.exit(1)
else:
    base_folder = sys.argv[1]

endpoint = toml.load("config.toml")
ENDPOINT = endpoint["UUID"]
FOLDER = endpoint["FOLDER"]
DOMAIN = endpoint["DOMAIN"]

# The portal can support multiple data releases, each including datasets
RELEASE_NAME = "index"

dsets = ["cmb", "synch", "dust"]


# from https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


def get_fileinfo(fname):
    """Parse file metadata from filename"""
    freq = fname.split(".")[0].split("_")[1].replace("GHz", "")
    return freq


def write_dataset(dset, n_files, data_size, file_table_rows):
    dset_table_header = ["File Name", "Frequency Band (GHz)", "Size"]
    writer = MarkdownTableWriter(
        headers=dset_table_header, value_matrix=file_table_rows, margin=1
    )

    dsettext = dset.replace("_", " ")

    dset_text = f"""---
title: "Dataset: PySM Simulations {dsettext}"
author: "PySM development team"
description: "PySM Simulations {dset}"
date_created: "2024-09-12"
seo:
  type: Dataset
---

[Back to release](./{RELEASE_NAME}.html#datasets)
See [data access](./{RELEASE_NAME}.html#data-access) on the Data Release page.

Access the data through the Globus web interface: [![Download via Globus](images/globus-logo.png)](https://app.globus.org/file-manager?origin_id={ENDPOINT}&origin_path=%2F{FOLDER}%2F{dset}%2F)

Download the [file manifest](https://{DOMAIN}/{FOLDER}/{dset}/manifest.json) for the exact file sizes and checksums.

## Files

- Number of files: {n_files}
- Total size: {data_size}
- [JSON format file manifest](https://{DOMAIN}/{FOLDER}/{dset}/manifest.json)

"""

    with open(f"{RELEASE_NAME}-{dset}.md", "w") as f:
        f.write(dset_text)
        f.write(writer.dumps())


dsets_table_header = ["Link", "Dataset", "Number of Files", "Total Size"]
dsets_table_data = []

for dset in dsets:
    dset_table_data = []
    # load file list
    # with open(f'{RELEASE_NAME}-{dset}.json') as f: # use this for multiple releases

    manifest_path = f"{base_folder}/{dset}/manifest.json"
    with open(manifest_path) as f:
        file_data = json.load(f)
    # loop over files, build file table info for dataset
    # remove manifest from list
    # total up bytes in dataset
    total_bytes = 0
    n_files = len(file_data)
    # sort file_entry by filename
    file_data = sorted(file_data, key=lambda x: x["filename"])
    for file_entry in file_data:
        file_path = file_entry["filename"]
        file_name = file_path.split("/")[-1]
        total_bytes += file_entry["length"]
        fsize = sizeof_fmt(file_entry["length"])
        freq = get_fileinfo(file_name)
        flink = f"[`{file_name}`](https://{DOMAIN}/{file_path})"
        dset_table_data.append([flink, freq, fsize])
    dset_size = sizeof_fmt(total_bytes)
    write_dataset(dset, n_files, dset_size, dset_table_data)
    dset_url = f"[Link]({RELEASE_NAME}-{dset}.html)"
    dsets_table_data.append([dset_url, f"{dset}", f"`{n_files}`", dset_size])

writer = MarkdownTableWriter(
    headers=dsets_table_header, value_matrix=dsets_table_data, margin=1
)

with open(RELEASE_NAME + ".md", "a") as f:
    f.write(writer.dumps())
