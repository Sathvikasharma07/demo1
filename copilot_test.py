import os
import platform
import subprocess

def get_system_uptime():
    system = platform.system()
    if system == "Windows":
        # Use 'net stats srv' and parse output for 'Statistics since'
        try:
            output = subprocess.check_output("net stats srv", shell=True, text=True)
            for line in output.splitlines():
                if "Statistics since" in line:
                    return f"System uptime (since): {line.split('since')[1].strip()}"
        except Exception as e:
            return f"Error retrieving uptime: {e}"
    elif system == "Linux" or system == "Darwin":
        try:
            # Use the 'uptime' command
            output = subprocess.check_output("uptime -p", shell=True, text=True)
            return f"System uptime: {output.strip()}"
        except Exception as e:
            return f"Error retrieving uptime: {e}"
    else:
        return "Unsupported operating system"

if __name__ == "__main__":
    print(get_system_uptime())
