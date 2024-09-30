#!/usr/bin/env python

import json
import sys
from pytablewriter import MarkdownTableWriter
import toml

config = toml.load("config.toml")

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
    try:
        freq = fname.split(".")[0].split("_")[1].replace("GHz", "")
    except IndexError:
        freq = "0"
    return freq


def write_dataset(dset, n_files, data_size, file_table_rows):
    dset_table_header = ["File Name", "Frequency Band (GHz)", "Size"]
    writer = MarkdownTableWriter(
        headers=dset_table_header, value_matrix=file_table_rows, margin=1
    )

    metadata = toml.load("metadata.toml")
    dset_text = "---\n"
    for k, v in metadata.items():
        dset_text += f"{k}: {v.format(dset=dset)}\n"

    dset_text += f"""
seo:
  type: Dataset
---

[Back to release](./{RELEASE_NAME}.html#datasets)
See [data access](./{RELEASE_NAME}.html#data-access) on the Data Release page.

Access the data through the Globus web interface: [![Download via Globus](images/globus-logo.png)](https://app.globus.org/file-manager?origin_id={config["UUID"]}&origin_path=%2F{config["FOLDER"]}%2F{dset}%2F)

Download the [file manifest](https://{config["DOMAIN"]}/{config["FOLDER"]}/{dset}/manifest.json) for the exact file sizes and checksums.

## Files

- Number of files: {n_files}
- Total size: {data_size}
- [JSON format file manifest](https://{config["DOMAIN"]}/{config["FOLDER"]}/{dset}/manifest.json)

"""

    output_path = f"{RELEASE_NAME}-{dset}.md"
    print(f"Writing dataset markdown to {output_path}")
    with open(output_path, "w") as f:
        f.write(dset_text)
        f.write(writer.dumps())


dsets_table_header = ["Link", "Dataset", "Number of Files", "Total Size"]
dsets_table_data = []

for dset in dsets:
    header = f"Creating markdown for dataset {dset}"
    print("*" * len(header))
    print(header)
    print("*" * len(header))
    dset_table_data = []
    # load file list
    # with open(f'{RELEASE_NAME}-{dset}.json') as f: # use this for multiple releases

    manifest_path = f"{dset}-manifest.json"
    print(f"Reading manifest: {manifest_path}")
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
        print("adding file", file_path)
        file_name = file_path.split("/")[-1]
        total_bytes += file_entry["length"]
        fsize = sizeof_fmt(file_entry["length"])
        freq = get_fileinfo(file_name)
        flink = f"[`{file_name}`]({file_entry['url']})"
        # uncomment to enable visualization of images for the jpg files
        # if flink.endswith(".jpg)") and dset in ["dust", "synch"]:
        #    flink = "!" + flink
        dset_table_data.append([flink, freq, fsize])
    dset_size = sizeof_fmt(total_bytes)
    write_dataset(dset, n_files, dset_size, dset_table_data)
    dset_url = f"[Link]({RELEASE_NAME}-{dset}.html)"
    dsets_table_data.append([dset_url, f"{dset}", f"`{n_files}`", dset_size])

writer = MarkdownTableWriter(
    headers=dsets_table_header, value_matrix=dsets_table_data, margin=1
)
print("> Appending summary table to", RELEASE_NAME + ".md")
with open(RELEASE_NAME + ".md", "a") as f:
    f.write(writer.dumps())
