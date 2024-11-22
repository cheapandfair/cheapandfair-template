#  Cheap&FAIR data portal template

Cheap&FAIR has a Template Github repository that can be used to create the basic structure of the Data Portal website.

In this tutorial we will create a new data portal based on the Cheap&FAIR template.

**Requirements:**

* A Github account
* A Globus account
* A Globus Guest Collection with writing permissions

In the tutorial we will first configure Github pages to serve the static website, then we will copy a test dataset to your own Globus Collection and then populate the website with metadata and links to the data hosted on Globus.

## Configure the Github pages repository

The static website will be hosted on Github pages and Github will automatically run Jekyll at each commit to transform the input Markdown pages to HTML files.

Login to Github and go to <https://github.com/cheapandfair/cheapandfair-template>

Click on the "Use this template" button and create a new repository in your account.

### Configure Github Pages

The only steps necessary to configure Github pages is:

1. Go to the repository settings
2. Scroll down to the Github Pages section
3. Select the `main` branch and the leave the default `/ (root)` folder
4. Click on the "Save" button
5. The website will be available in a few minutes at `https://<github_username>.github.io/cheapandfair-template`


### Clone the repository locally

Finally we need to clone the repository locally to be able to edit the files.
Using the Github-CLI `gh`, which you can download from <https://cli.github.com/>, you can clone the repository with the following command:


```python
!gh repo clone cheapandfair-template
```

## Configure the Globus guest collection

We assume here that you have writing permissions to a Globus guest collection that you want to use to store and publish the data, and that you have a "source" Globus endpoint that you will transfer the data from.
So we simulate for example having data on a local Globus endpoint close to the data source, and we want to transfer the data to a guest collection that is shared with collaborators and the public.

## Copy data to the Globus guest collection


First create a `config.toml` file in the root of the repository with the following content:
Customize the `UUID`, `FOLDER` and `DOMAIN` fields with the values of your Globus Guest Collection from the "Overview" page:

```toml
# The following refer to the destination collection, where the data will be copied to and that will serve as backend for the data portal
UUID='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
FOLDER='/datasets/'
DOMAIN='xxxxxxxx.c2d0f8.bd7c.data.globus.org'
# collection of the source data, during the tutorial this is the "Cheap and FAIR Tutorial Datasets" collection
SOURCE_UUID='7352d991-b0a0-49a2-830c-e8fe8c968ca2'
SOURCE_FOLDER='/public/datasets/'
```
## Authenticate with Globus

Login to Globus using the following command. It can be executed in a Jupyter Notebook or in a IPython terminal.

This will open a browser window where you can login to Globus and receive a token to paste back into the notebook.


```python
import copy_dataset
copy_dataset.login();
```

## Copy Datasets and create manifests
We copy the dataset by providing the name of the dataset, the UUID of the destination Guest Collection, and the folder we want it copied to.

The method will return the manifest of the files that were copied and will also write a copy of the manifest to the local directory named `{dataset}-manifest.json`.


```python
cmb_manifest = copy_dataset.copydataset('cmb')
```

Let's look at a couple of the entries in the file manifest.


```python
import json
print(json.dumps(cmb_manifest[:2], indent=2))
```

Now we can copy the other two datasets. You won't need to login again because the tokens have been cached in `~/.cheapandfair.json`. In case the token in the file have expired you can just delete the file and run the `login()` function again.


```python
dust_manifest = copy_dataset.copydataset('dust')
synch_manifest = copy_dataset.copydataset('synch')
synch_manifest = copy_dataset.copydataset('cmb_spectra')
synch_manifest = copy_dataset.copydataset('dust_synch_spectra')
```

We can see that the manifests were saved locally.


```python
!ls *.json
```

## Viewing your Data

Let's look at your Collection and see how the datasets are arranged and then set permissions on the folders. Evaluate the next cell and click the link to see your Collection in the File Manager view.


```python
import toml
config = toml.load("config.toml")
url = f'https://app.globus.org/file-manager?origin_id={config["UUID"]}&two_pane=false'
print(url)
```

You should see a listing of the files and folders in your Collection. You can double click on the folder you specified earlier (e.g., `/datasets/`) and see each dataset folder.

<div>
<img alt="Screenshot of a Globus Collection file listing" src="./img/caribou.png" style="width: 50%; height: 50%" />
</div>

If you go into a particular folder you can see files in it. Dataset folders can have subfolder, although these example datasets have files only in one folder.

<div>
<img alt="Screenshot of a Globus Collection file listing" src="./img/caribou-cmb.png" style="width: 50%; height: 50%" />
</div>


## Setting Permissions

Globus Guest Collections allow you to set permissions on a folder level. All of the subfolder inherit the permission of the higher level folder, so you be less restrictive on subfolders, but you cannot reduce access to a subfolder. This is why the SRDR model suggests that all datasets have a "top" folder, even if the dataset has subfolders. This way you can assign permissions on a per-dataset basis.

To see and manage the permission on the Guest Collection, click the "Permissions" link in the File Manager.

<div>
<img alt="Screenshot of a Globus Collection file listing" src="./img/permissions-button.png" style="width: 50%; height: 50%" />
</div>

The permissions page for each Collection has a consistent URL. You can also evaluate the cell below and click the link.


```python
perm_url = f'https://app.globus.org/file-manager/collections/{config["UUID"]}/sharing'
print(perm_url)
```

In the permissions tab you can manage the permissions by clicking the "Add Permissions -- Share With" button on the right. You may need to provide another consent.

<div>
<img alt="Screenshot of a Globus Collection permission list" src="./img/share-with.png" style="width: 50%; height: 50%" />
</div>

Again, the URL is consistent so you can use the cell below to create a link directly to the add permissions window.


```python
add_perm_url = f'https://app.globus.org/file-manager/collections/{config["UUID"]}/sharing/create'
print(add_perm_url)
```

There are five datasets and you'll set permissions on each of them as follows:

- `cmb`: Read-only by the Group you created
- `cmb_spectra`: Read-only by the Group you created
- `dust`: Read-only by the public (anonymous access)
- `synch`: Read-only by the public (anonymous access)
- `dust_synch_spectra`: Read-only by the public (anonymous access)

Permissions can be managed using the Globus API via the Python and JavaScript SDKS, or using the Globus CLI. We're using the webapp user interface so that you have a way to quickly check the state of the permissions at all times.

We'll start with the `cmb` dataset to show how to add read access by a Group.

- Use the "Browse" button to select that folder.
- Set the type of entity to share with "group".
- Use the "Select a Group" button to choose your Group.
- Click the "Add Permission" button at the bottom.
- At the prompt, agree to add another permission.

<div>
<img alt="Screenshot of adding a permission to a Globus Collection" src="./img/cmb-perms.png" style="width: 50%; height: 50%" />
</div>

Next, we'll make the `dust` dataset public.

- Use the "Browse" button to select that folder.
- Set the type of entity to share with "public (anonymous)".
- Click the "Add Permission" button at the bottom.
- At the prompt, agree to add another permission.

<div>
<img alt="Screenshot of adding a permission to a Globus Collection" src="./img/dust-perms.png" style="width: 50%; height: 50%" />
</div>

Go through the other datasets and add permission according to the list above. When you're done, you can review the permissions on your datasets by checking the permission tab.

<div>
<img alt="Screenshot of a Globus Collection permission list" src="./img/all-perms.png" style="width: 50%; height: 50%" />
</div>

You should have one permission line per dataset.

If you need to you can remove permissions by deleting them. You can't edit a permission and if you move the data, the permissions don't follow it. 

## Create markdown pages

Now that the metadata of all the files within a dataset are available in the JSON files we created in the step before, we can create markdown pages for each dataset. These will then be compiled by Jekyll into the final website.

The `2_create_markdown.py` Python script needs to be customized for each release of datasets, it needs the path to the datasets to loop through them, then creates Markdown pages based on a template included in the script itself.

Once the Markdown pages are generated, they are added to the repository and they do not need to be generated again unless the datasets change.

From the perspective of the data portal, there is no difference  between a public and a private dataset, their metadata are published in any case, the difference is that when a user tries to download a private dataset, they are redirected to the Globus login page.


The current version of `create_markdown.py` reads metadata about a page from `metadata.json`, it customizes it with the value of the `dset` variable and writes it to a file named `index-{dset}.md`.


```python
%%file metadata.toml
# {dset} will be replaced with the dataset name
title="Dataset - Cosmic Microwave Background Simulations {dset}"
author="Author Name"
description="Maps in FITS format and HEALPix pixelization and map preview in jpg format for the {dset} component"
date_created="2024-09-12"
```


```python
%ls *manifest*
```


```python
%run create_markdown.py
```


```python
%ls *.md
```

It also appends a table at the bottom of `index.md` with total size and link of each dataset page.


```python
!git diff index.md
```

We can finally add the Markdown files to the repository and push them to GitHub, then check that the data portal website has been updated.


```python
!git config --global user.email "Email"
!git config --global user.name "Name"
```


```python
!git add index*
!git commit -m "Add datasets markdown files"
```


```python
!git push
```

## Advanced topics

For further customization of the data portal, see the notebooks 4 to 7 of the [Cheap&FAIR Data Portal Tutorial](https://github.com/cheapandfair/cheapandfair-gateways-2024):

* 4. Check the JSON-LD metadata and download datasets in batch using BDBag
* 5. Add new static pages, images once or programmatically on all datasets
* 6. Visualize binary files with Pyodide or plot CSV files with `chart.js`
* 7. Use Globus groups to handle permissions and allow data access/visualization only to specific users
