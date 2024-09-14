#!/bin/bash
dataset=$1
source ROOT.sh
globus ls -lrF json $ROOT/$dataset/ > $dataset.json
