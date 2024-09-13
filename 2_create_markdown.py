#!/usr/bin/env python

import json
from pytablewriter import MarkdownTableWriter

ENDPOINT = '18ed636e-0389-44c3-b533-cb3901dfc60f' # UUID
DOMAIN = 'g-1926f5.c2d0f8.bd7c.data.globus.org'
FOLDER = 'data'
# The portal can support multiple data releases, each including datasets
RELEASE_NAME = 'index'

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
    freq = fname.split(".")[0].split("_")[1].replace("GHz","")
    return freq

def write_dataset(dset, n_files, data_size, file_table_rows):
    dset_table_header = ["File Name", "Frequency Band (GHz)", "Size"]
    writer = MarkdownTableWriter(
        headers=dset_table_header,
        value_matrix=file_table_rows,
        margin=1
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

    with open(f'{RELEASE_NAME}-{dset}.md', 'w') as f:
        f.write(dset_text)
        f.write(writer.dumps())


dsets_table_header = ["Link", "Dataset", "Number of Files", "Total Size"]
dsets_table_data = []

for dset in dsets:
    dset_table_data = []
    # load file list
    # with open(f'{RELEASE_NAME}-{dset}.json') as f: # use this for multiple releases
    with open(f'{dset}.json') as f:
        file_data = json.load(f)
        file_list = file_data["DATA"]
        # loop over files, build file table info for dataset
        # remove manifest from list
        # total up bytes in dataset
        total_bytes = 0
        n_files = len(file_list) - 1
        for file_entry in file_list:
            fname = file_entry['name']
            if not fname == 'manifest.json':
                total_bytes += file_entry['size']
                fsize = sizeof_fmt(file_entry['size'])
                freq = get_fileinfo(fname)
                flink = f'[`{fname}`](https://{DOMAIN}/{FOLDER}/{dset}/{fname})'
                dset_table_data.append([flink, freq, fsize])
        dset_size = sizeof_fmt(total_bytes)
        write_dataset(dset, n_files, dset_size, dset_table_data)
        dset_url = f'[Link]({RELEASE_NAME}-{dset}.html)'
        dsets_table_data.append([dset_url, f'{dset}', f'`{n_files}`', dset_size])

writer = MarkdownTableWriter(
    headers=dsets_table_header,
    value_matrix=dsets_table_data,
    margin=1
    )

with open(RELEASE_NAME + '.md', 'a') as f:
    f.write(writer.dumps())
