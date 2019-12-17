#!/bin/bash

nbatches=$1
jobsperbatch=$2
run=$3
file=$4
today=`date +%Y-%m-%d`

module load jaspy

logdir=/home/users/rpetrie/cmip6/cmip6-replica-mgmt/lotus-logs/${today}-${run}

mkdir -p $logdir

for batch in $(seq 0 $nbatches); do
    bsub -o ${logdir}/%J.out -W 22:00 python /home/users/rpetrie/cmip6/cmip6-replica-mgmt/scripts/run_verify_lotus.py ${batch} ${jobsperbatch} ${file}
done