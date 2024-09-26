#!/usr/bin/env bash
echo "PYTHONPATH is ${PYTHONPATH}"

job=$1
alpha=$2
threads=$3
n_clients=$4

# specify output workdir
RESULT_ROOT=/lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/tmp/sim_cifar10
out_workspace=${RESULT_ROOT}/${job}_alpha${alpha}

# TODO: remove, this is just a check since something with nvflare pathing isn't right
cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/cifar10-sim
pip install -r requirements.txt

# use my amd nvflare repo
pip install -e /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare

# run FL simulator
./set_alpha.sh "${job}" "${alpha}"
echo "Running ${job} using FL simulator with ${threads} threads and ${n_clients} clients. Save results to ${out_workspace}"
nvflare simulator "jobs/${job}" --workspace "${out_workspace}" --threads "${threads}" --n_clients "${n_clients}" --gpu 0,1,2,3,4,5,6,7
