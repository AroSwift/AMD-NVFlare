#!/bin/bash
#SBATCH --mail-user=abarlow505@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -A STF040
#SBATCH -J ROCM-GPU-CHECK
#SBATCH -o %x-%j.out
#SBATCH -t 00:5:00
#SBATCH -p batch
#SBATCH -N 1
#SBATCH -q debug

GPUS=8
CORES=56

CMD="python test.py"

srun --gpus-per-node=${GPUS} -c${CORES} --ntasks-per-node=1 ${CMD}