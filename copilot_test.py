import platform
import subprocess
import sys

def get_system_uptime():
    system = platform.system()
    try:
        if system == "Windows":
            # Use 'wmic' for more robust output
            output = subprocess.check_output(
                'wmic os get lastbootuptime', shell=True, text=True, stderr=subprocess.DEVNULL
            )
            lines = output.strip().splitlines()
            if len(lines) > 1:
                boot_time_raw = lines[1].strip()
                # Format: YYYYMMDDHHMMSS.MMMMMM+timezone
                from datetime import datetime
                boot_time_str = boot_time_raw[:14]  # up to seconds
                boot_time = datetime.strptime(boot_time_str, "%Y%m%d%H%M%S")
                now = datetime.now()
                uptime = now - boot_time
                return f"System uptime: {str(uptime).split('.')[0]}"
            else:
                return "Could not determine system uptime."
        elif system in ("Linux", "Darwin"):
            # Try 'uptime -p' first, fallback to /proc/uptime for Linux
            try:
                output = subprocess.check_output("uptime -p", shell=True, text=True, stderr=subprocess.DEVNULL)
                return f"System uptime: {output.strip()}"
            except Exception:
                if system == "Linux":
                    with open("/proc/uptime", "r") as f:
                        seconds = float(f.readline().split()[0])
                        mins, sec = divmod(int(seconds), 60)
                        hrs, mins = divmod(mins, 60)
                        days, hrs = divmod(hrs, 24)
                        return (
                            f"System uptime: {days} days, {hrs} hours, {mins} minutes, {sec} seconds"
                        )
                else:
                    return "Could not determine uptime for this system."
        else:
            return "Unsupported operating system."
    except Exception as e:
        return f"Error retrieving uptime: {e}"

if __name__ == "__main__":
    print(get_system_uptime())
