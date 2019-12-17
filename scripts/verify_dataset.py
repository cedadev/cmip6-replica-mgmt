#!/usr/bin/env Python

import os
import sys
import query_solr

RETRACTED_LOGDIR = "../logs/retracts"
FATAL_LOGDIR = "../logs/fatals"

LOGDIRS = [RETRACTED_LOGDIR, FATAL_LOGDIR]
CWD = os.getcwd()
for dir in LOGDIRS:
    ld = os.path.join(CWD, dir)
    if not os.path.exists(ld):
        os.makedirs(ld)

def write_logfile(dir, ds):

    os.chdir(dir)
    open(ds, 'a').close()


def verify_dataset_is_latest(ds, verbose=True):


    solr = query_solr.QuerySolr(verbose=False)
    dataset_version = int(ds.split('.')[-1].strip().lstrip('v'))
    res = solr.query_solr('.'.join(ds.split('.')[:-1]), query="master_id", type="Dataset",
                          return_fields="latest, replica, retracted, version, data_node")

    if verbose:
        print(res)

    if len(res) == 0:
        if verbose:
            print("NO RESULTS :: {}.format"(ds))
        write_logfile(RETRACTED_LOGDIR, ds)
    
    elif len(res) == 1:
        ## REPLICA COPIES
        if res[0]["replica"]:
            if res[0]["retracted"]:
                if verbose:
                    print("ONLY_RETRACTED :: {}.format"(ds))
                write_logfile(RETRACTED_LOGDIR, ds)
            else:
                if verbose:
                    print("ONLY_REPLICAS :: {}.format"(ds))
                write_logfile(RETRACTED_LOGDIR, ds)
    
        ## MASTER COPIES
        else: 
            if res[0]["retracted"]:
                if verbose:
                    print("ONE_MASTER_RETRACTED :: {}.format"(ds))
                write_logfile(RETRACTED_LOGDIR, ds)
            else:
                if verbose:
                    print("ONE_MASTER_EXIST :: {}.format"(ds))
                    # write_logfile("logs/master_copies_exist.txt", ds)



    else: # multiples
        master_copy = [r for r in res if not r["replica"]]
        if verbose:
            print(master_copy)

        if len(master_copy) == 0:
            if verbose:
                print("MISSING_MASTER :: {}".format(ds))
            write_logfile(FATAL_LOGDIR, ds)

        latest_version = max([int(ds['version']) for ds in master_copy if ds["latest"]])
        print("latest_version {}, dataset_version {}".format(latest_version, dataset_version))
        if latest_version == dataset_version:
            if verbose:
                print("LATEST_VERSION :: {}".format(ds))
        else:
            if verbose:
                print("NOT_LATEST_VERSION :: {}".format(ds))
            write_logfile(RETRACTED_LOGDIR, ds)



if __name__ == "__main__":

    dataset_id = sys.argv[1]
    verify_dataset_is_latest(dataset_id)