#!/usr/bin/env Python

import os
from sys import argv
from subprocess import call

start = int(argv[1])
PER_BATCH = int(argv[2])
datasets_file = argv[3]

srt_idx = start * PER_BATCH
end_idx = srt_idx + PER_BATCH

with open(datasets_file, 'r') as fr:
    datasets = fr.readlines()

for ds in datasets[srt_idx: end_idx]:
    run_cmd = ["python", "/home/users/rpetrie/cmip6/cmip6-replica-mgmt/scripts/verify_dataset.py", ds.strip()]
    run = call(run_cmd)