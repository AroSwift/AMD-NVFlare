#!/bin/bash
#SBATCH --mail-user=barlowat@ornl.gov
#SBATCH --mail-type=ALL
#SBATCH -A STF040
#SBATCH -J AMD-NVFLARE-SIMULATOR
#SBATCH -o %x-%j.out
#SBATCH -t 01:00:00
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -q debug

GPUS=8
CORES=56

hostname

module load PrgEnv-gnu/8.5.0
module load miniforge3/23.11.0-0
module load PrgEnv-cray
module load rocm/5.5.1

export PYTHONPATH=${PWD}/..

cd ~

conda init bash
conda activate python3-10-11


cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare
pip install -r requirements.txt

cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/cifar10-sim
pip install -r requirements.txt

# bash prepare_data.sh



export PYTHONPATH=${PWD}/..
CUDA_VISIBLE_DEVICES=
HIP_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

echo $CUDA_VISIBLE_DEVICES

echo $HIP_VISIBLE_DEVICES

echo $PATH

# ./run_simulator.sh cifar10_central 0.0 1 1
srun --gpus-per-node=${GPUS} -c${CORES} --ntasks-per-node=1 /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/cifar10-sim/run_simulator_with_gpus.sh cifar10_central 0.0 1 1

# Run with
# sbatch test_simulator_with_gpus_batch_script.sl

# View with
# squeue -l -u aroswift