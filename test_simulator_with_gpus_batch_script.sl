#!/bin/bash
#SBATCH --mail-user=barlowat@ornl.gov
#SBATCH --mail-type=ALL
#SBATCH -A STF040
#SBATCH -J AMD-NVFLARE-SIMULATOR
#SBATCH -o %x-%j.out
#SBATCH -t 00:15:00
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -q debug

hostname
# module load PrgEnv-gnu/8.3.3
module load PrgEnv-gnu/8.5.0
# module load miniforge3/24.3.0-0
module load miniforge3/23.11.0-0
module load PrgEnv-cray
# module load cpe/23.09
module load rocm/5.5.1

# export PYTHONPATH=${PWD}/..

conda init
conda activate python3-10-11


cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare


# export PYTHONPATH="/lustre/orion/stf040/scratch/aroswift/envs/python3-10-11/bin/python"
# ${PWD}/..

# conda config --append envs_dirs /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare
# conda config --append envs_dirs /lustre/orion/stf040/scratch/aroswift/envs
# source activate base
pip install -r requirements.txt

cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/cifar10-sim
pip install -r requirements.txt


export PYTHONPATH=${PWD}/..
CUDA_VISIBLE_DEVICES=

./run_simulator.sh cifar10_central 0.0 1 1

# Run with
# sbatch test_simulator_with_gpus_batch_script.sl

# View with
# squeue -l -u aroswift