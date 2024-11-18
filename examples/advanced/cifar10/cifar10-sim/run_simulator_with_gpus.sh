#!/usr/bin/env bash
echo "PYTHONPATH is ${PYTHONPATH}"

job=$1
alpha=$2
threads=$3
n_clients=$4

# specify output workdir
RESULT_ROOT=/lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/tmp/sim_cifar10
out_workspace=${RESULT_ROOT}/${job}_alpha${alpha}

# # TODO: remove, this is just a check since something with nvflare pathing isn't right
# cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/cifar10-sim
# pip install -r requirements.txt

# # use my amd nvflare repo
# pip install -e /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare






hostname

# module load PrgEnv-gnu/8.5.0
# module load miniforge3/23.11.0-0
# module load PrgEnv-cray
# module load rocm/5.5.1


# NEW ATTEMPT
module purge
module load PrgEnv-gnu/8.5.0
# module load rocm/5.5.1
module load rocm/6.2.4
module load miniforge3/23.11.0-0

module avail


# export PYTHONPATH=${PWD}/..
export PYTHONPATH=${PYTHONPATH}:/lustre/orion/stf040/scratch/aroswift/AMD-NVFlare

cd ~

# # conda init bash
# conda init
# conda activate python3-10-11

# new attempts:
# Initialize Conda for the current shell
source /sw/frontier/miniforge3/23.11.0-0/etc/profile.d/conda.sh

# Activate the desired Conda environment
conda activate python3-10-11

export PATH=$PATH:/ccs/home/aroswift/.local/23.11.0-0/bin
export PYTHONPATH=/lustre/orion/stf040/scratch/aroswift/AMD-NVFlare:$PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/tmp
export PYTHONPATH=$PYTHONPATH:/lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced
export PYTHONPATH=$PYTHONPATH:/lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10
export PYTHONPATH=$PYTHONPATH:/lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/cifar10-sim
export PYTHONPATH=$PYTHONPATH:/lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/pt
export PYTHONPATH=/lustre/orion/stf040/scratch/aroswift/pip_packages:$PYTHONPATH


echo "PYTHONPATH is $PYTHONPATH"

export AMD_GPU=True
echo "AMD_GPU is $AMD_GPU"



# watch -n 10 rocm-smi > /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/gpu_usage.log &


# cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare
# pip3 install -r requirements.txt
# pip3 install .

# cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/cifar10-sim
# pip3 install -r requirements.txt

# cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare
# pip install -r /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/requirements.txt
# pip install /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare
# pip install -r /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/cifar10-sim/requirements.txt

# cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/cifar10-sim
# bash ./prepare_data.sh



cd /lustre/orion/stf040/scratch/aroswift/AMD-NVFlare/examples/advanced/cifar10/cifar10-sim


# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.5

# python -c "import torch; print(torch.__version__); print(torch.backends.mps.is_available()); print(torch.backends.hip.is_available())"

# # If this prints CUDA available: False or GPU count: 0, the GPUs aren't being detected by PyTorch in the job's environment.
# python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU count:', torch.cuda.device_count())"


# python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('HIP backend available:', torch.backends.hip.is_available()); print('GPU count:', torch.cuda.device_count())"


# HIP_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
# echo "NVFlare GPUs visible: $(HIP_VISIBLE_DEVICES=$HIP_VISIBLE_DEVICES python -c 'import torch; print(torch.cuda.device_count())')"

echo "checking pytorch availability..."
python -c "import torch; print('PyTorch Version:', torch.__version__); print('HIP backend available:', hasattr(torch.backends, 'hip')); print('CUDA available:', torch.cuda.is_available()); print('GPU count:', torch.cuda.device_count())"
# should return something like:
# PyTorch Version: 2.1.2+rocm5.5
# HIP backend available: False
# CUDA available: True
# GPU count: 1


export NVFLARE_DEBUG_LOGGING=1

export MIOPEN_LOG_LEVEL=5
# export MIOPEN_USER_DB_PATH=~/.cache/miopen
export MIOPEN_USER_DB_PATH=/lustre/orion/stf040/scratch/aroswift/miopen_cache
export MIOPEN_DISABLE_SQLITE=1
export MIOPEN_DISABLE_CACHE=1


# rocminfo

# run FL simulator
./set_alpha.sh "${job}" "${alpha}"
echo "Running ${job} using FL simulator with ${threads} threads and ${n_clients} clients. Save results to ${out_workspace}"
nvflare simulator "jobs/${job}" --workspace "${out_workspace}" --threads "${threads}" --n_clients "${n_clients}" --gpu 0,1,2,3,4,5,6,7
