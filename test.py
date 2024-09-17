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
