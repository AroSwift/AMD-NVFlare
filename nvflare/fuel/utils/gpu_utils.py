# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import subprocess
from typing import List, Dict, Optional
from shutil import which
import json


# TODO: convert this to some form of env var or config setting
AMD_GPU = True


# Nvidia GPU-Specific Utils

def has_nvidia_smi() -> bool:
    from shutil import which

    return which("nvidia-smi") is not None

def use_nvidia_smi(query: str, report_format: str = "csv"):
    if has_nvidia_smi():
        result = subprocess.run(
            ["nvidia-smi", f"--query-gpu={query}", f"--format={report_format}"],
            capture_output=True,
            text=True,
        )
        rc = result.returncode
        if rc > 0:
            raise Exception(f"Failed to call nvidia-smi with query {query}", result.stderr)
        else:
            return result.stdout.splitlines()
    return None

def _parse_gpu_mem(result: str = None, unit: str = "MiB") -> List:
    gpu_memory = []
    if result:
        for i in result[1:]:
            mem, mem_unit = i.split(" ")
            if mem_unit != unit:
                raise RuntimeError("Memory unit does not match.")
            gpu_memory.append(int(mem))
    return gpu_memory

def get_nvidia_host_gpu_memory_total(unit="MiB") -> List:
    result = use_nvidia_smi("memory.total")
    return _parse_gpu_mem(result, unit)

def get_nvidia_host_gpu_memory_free(unit="MiB") -> List:
    result = use_nvidia_smi("memory.free")
    return _parse_gpu_mem(result, unit)

def get_nvida_host_gpu_ids() -> List:
    """Gets GPU IDs.

    Note:
        Only supports nvidia-smi now.
    """
    result = use_nvidia_smi("index")
    gpu_ids = []
    if result:
        for i in result[1:]:
            gpu_ids.append(int(i))
    return gpu_ids



# AMD GPU-Specific Utils

def run_command(command: List[str]) -> Optional[str]:
    # Executes a command and returns the output as a string
    if which(command[0]):
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to run command: {' '.join(command)}", result.stderr)
        return result.stdout
    return None

def get_amd_gpu_host_ids() -> List[str]:
    # Returns an array of host IDs using `rocm-smi --showmeminfo vram --json`
    result = run_command(["rocm-smi", "--showmeminfo", "vram", "--json"])
    host_ids = []

    if result:
        try:
            gpu_data = json.loads(result)
            # Extract the keys from the JSON object. E.g. 'card0', 'card1', ...
            host_ids = list(gpu_data.keys())
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Output was: {result}")
    else:
        print("No output from `rocm-smi --showmeminfo vram --json` command")
        print("No AMD GPUs identified")

    return host_ids

def get_amd_gpu_memory_info() -> Dict[str, List[int]]:
    # Returns total and free memory in MiB using `rocm-smi --showmeminfo vram --json`
    result = run_command(["rocm-smi", "--showmeminfo", "vram", "--json"])
    memory_info = {"total": [], "free": []}

    if result:
        try:
            gpu_data = json.loads(result)
            for gpu_id, gpu in gpu_data.items():
                total_mem = int(gpu.get("VRAM Total Memory (B)", 0)) // (1024 * 1024)  # Convert bytes to MiB
                used_mem = int(gpu.get("VRAM Total Used Memory (B)", 0)) // (1024 * 1024)  # Convert bytes to MiB
                free_mem = total_mem - used_mem
                memory_info["total"].append(total_mem)
                memory_info["free"].append(free_mem)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Output was: {result}")
            print("AMD GPU Memory info not identified")

    return memory_info

def get_amd_gpu_memory_total() -> List[int]:
    # Returns the total memory of each GPU in MiB
    memory_info = get_amd_gpu_memory_info()
    return memory_info["total"]

def get_amd_gpu_memory_free() -> List[int]:
    # Returns the free memory of each GPU in MiB
    memory_info = get_amd_gpu_memory_info()
    return memory_info["free"]



# Usable 

def get_host_gpu_ids() -> List[str]:
    if AMD_GPU:
        return get_amd_host_ids()
    else:
        return get_nvida_host_gpu_ids()

def get_host_gpu_memory_free(unit="MiB") -> List:
    if AMD_GPU:
        return get_amd_gpu_host_ids()
    else:
        return get_nvidia_host_gpu_memory_free(unit=unit)

def get_host_gpu_memory_total() -> List[str]:
    if AMD_GPU:
        return get_amd_gpu_memory_total()
    else:
        return get_nvidia_host_gpu_memory_total()