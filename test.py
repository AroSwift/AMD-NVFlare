# Aaron Barlow's tests of grabbing AMD host GPU ids, free memory, and total memory

import subprocess
import json
from typing import List, Dict, Optional
from shutil import which

def run_command(command: List[str]) -> Optional[str]:
    # Executes a command and returns the output as a string
    if which(command[0]):
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to run command: {' '.join(command)}", result.stderr)
        return result.stdout
    return None

def get_amd_host_ids() -> List[str]:
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

def pretty_print_gpu_info(gpu_ids: List[str], total_memory: List[int], free_memory: List[int]) -> None:
    # Prints GPU host IDs, total memory, and free memory in a readable format
    for idx, host_id in enumerate(gpu_ids):
        print(f"GPU {idx + 1}:")
        print(f"  Host ID: {host_id}")
        print(f"  Total Memory: {total_memory[idx]} MiB")
        print(f"  Free Memory: {free_memory[idx]} MiB")
        print("\n")

# Example usage
if __name__ == "__main__":
    host_ids = get_amd_host_ids()
    total_memory = get_amd_gpu_memory_total()
    free_memory = get_amd_gpu_memory_free()
    
    pretty_print_gpu_info(host_ids, total_memory, free_memory)
