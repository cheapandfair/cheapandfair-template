#!/bin/bash
dataset=$1
source ENDPOINT.sh
globus ls -lrF json $UUID:/$FOLDER/$dataset/ > $dataset.json
