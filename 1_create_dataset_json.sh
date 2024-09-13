#!/bin/bash
dataset=$1
globus ls -lrF json $ROOT/$dataset/ > $dataset.json
