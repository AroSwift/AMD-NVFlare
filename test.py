import subprocess
from typing import List, Dict
from shutil import which

def query_rocminfo() -> str:
    if which("rocminfo"):
        result = subprocess.run(
            ["rocminfo"],
            capture_output=True,
            text=True,
        )
        rc = result.returncode
        if rc > 0:
            raise Exception(f"Failed to call rocminfo", result.stderr)
        else:
            return result.stdout
    return None

def get_amd_gpu_info() -> List[Dict[str, str]]:
    result = query_rocminfo()
    gpu_info_list = []
    if result:
        lines = result.splitlines()
        current_agent = {}
        is_gpu = False

        for line in lines:
            line = line.strip()
            
            # Detect the start of a new agent block (assumption!)
            if line.startswith("*******"):
                if is_gpu and current_agent:
                    gpu_info_list.append(current_agent)
                
                current_agent = {}
                is_gpu = False
            
            if "Name:" in line:
                name = line.split(":")[1].strip()
                current_agent["Name"] = name
                if "gfx" in name or "Radeon" in name:
                    is_gpu = True
            
            if "Uuid:" in line:
                current_agent["Uuid"] = line.split(":")[1].strip()
            
            if "Node:" in line:
                current_agent["Node"] = line.split(":")[1].strip()

        # Only grab AMD GPUs
        if is_gpu and current_agent:
            gpu_info_list.append(current_agent)
    
    return gpu_info_list


def get_host_gpu_ids() -> List[int]:
    # grab the host gpu ids
    result = query_rocminfo()
    gpu_ids = []
    if result:
        lines = result.splitlines()
        gpu_index = 0

        for line in lines:
            line = line.strip()
            if "Name:" in line:
                name = line.split(":")[1].strip()
                if "gfx" in name.lower() or "radeon" in name.lower() or "gpu" in name.lower():
                    gpu_ids.append(gpu_index)
                    gpu_index += 1
    return gpu_ids

def _parse_gpu_mem(result: str, unit: str = "MiB") -> List[int]:
    # parse gpu memory
    gpu_memory = []
    lines = result.splitlines()

    for line in lines:
        if "Global memory size" in line:
            print(f"Debug: Found memory line: {line}")  # Debugging: Print the line to understand its format
            # Extract the memory size and convert to integer
            mem_str = line.split(":")[1].strip()
            mem_value = int(mem_str.split()[0])  # Get the numeric part
            mem_unit = mem_str.split()[1]        # Get the unit part

            # Check if units match
            if mem_unit != unit:
                raise RuntimeError(f"Memory unit does not match: expected {unit}, got {mem_unit}.")

            gpu_memory.append(mem_value)
    return gpu_memory

# TODO:
# def get_host_gpu_memory_total(unit: str = "MiB") -> List[int]:
#     result = query_rocminfo()
#     if result:
#         return _parse_gpu_mem(result, unit)
#     return []

# def get_host_gpu_memory_free(unit: str = "MiB") -> List[int]:
#     total_memory = get_host_gpu_memory_total(unit)
#     free_memory = [mem // 2 for mem in total_memory]  # Placeholder logic
#     return free_memory


def pretty_print_gpu_info(gpu_info_list: List[Dict[str, str]]) -> None:
    for idx, gpu_info in enumerate(gpu_info_list):
        print(f"GPU {idx + 1}:")
        print(f"  Name: {gpu_info.get('Name', 'N/A')}")
        print(f"  Uuid: {gpu_info.get('Uuid', 'N/A')}")
        print(f"  Node: {gpu_info.get('Node', 'N/A')}")
        print("\n")

# Example usage
if __name__ == "__main__":
    gpu_info = get_amd_gpu_info()
    pretty_print_gpu_info(gpu_info)

    gpu_ids = get_host_gpu_ids()
    print(f"GPU IDs: {gpu_ids}")
    
    # total_memory = get_host_gpu_memory_total()
    # print(f"Total GPU Memory: {total_memory} MiB")
    
    # free_memory = get_host_gpu_memory_free()
    # print(f"Free GPU Memory (Placeholder): {free_memory} MiB")
