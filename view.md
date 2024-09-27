---
title: "FITS map viewer"
author: "Cheap and Fair team"
description: "Demo data repository"
date_created: "2024-09-12"
---

<script src="https://cdn.jsdelivr.net/pyodide/v0.26.1/full/pyodide.js"></script>

<script type="text/javascript">
  async function main(){
    let pyodide = await loadPyodide();

await pyodide.loadPackage("micropip");
await pyodide.loadPackage("ssl");
const micropip = pyodide.pyimport("micropip");
await micropip.install('https://healpy.github.io/pyhealpy/dist/healpy-0.1.0-py3-none-any.whl');
await micropip.install('matplotlib');

pyodide.runPythonAsync(`
import js
from pyodide.ffi import to_js
from urllib.parse import urlparse
from urllib.parse import parse_qs


def get_url_parameters():
    # Get the current URL using JavaScript's window.location.href
    url = js.window.location.href

    parsed_url = urlparse(url)
    captured_value = parse_qs(parsed_url.query)["url"][0]
    return captured_value


import matplotlib

matplotlib.use("module://matplotlib_pyodide.wasm_backend")
import healpy as hp
import numpy as np

import matplotlib.pyplot as plt
from pyodide.http import pyfetch

url = get_url_parameters()
response = await pyfetch(url)
a = await response.bytes()
with open("a.fits", "wb") as f:
    f.write(a)
m = hp.read_map("a.fits")
hp.projview(m, coord=["G"], unit="uK_CMB", projection_type="mollweide")
plt.title(url.split("/")[-1])
plt.show()
`);
  }
  main();
</script>
