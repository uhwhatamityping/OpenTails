import platform, subprocess, psutil, time, sys, threading, os

host = platform.system()
host_ver = platform.release()

shell ="opentails-shell-r-0.1-september-5-26"

def update_screen():
    global uptime
    while True:
        uptime = time.time() - boot_time
        time.sleep(1)

def fetch_cpu_name():
    if sys.platform == "win32":
        cmd = "wmic cpu get name"
        output = subprocess.check_output(cmd, shell=True).decode()
        lines = [line.strip() for line in output.split("\n") if line.strip()]
        # lines[0] is the header "Name", lines[1] is the actual CPU name string
        return lines[1] if len(lines) > 1 else "Unknown CPU"

    elif sys.platform == "darwin":
        cmd = ["sysctl", "-n", "machdep.cpu.brand_string"]
        return subprocess.check_output(cmd).decode().strip()

    elif sys.platform.startswith("linux"):
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        # Grab the second part of the split (index 1) and strip it
                        return line.split(":")[1].strip()
        except (FileNotFoundError, IndexError):
            pass

    return "Unknown CPU"


# The CPU name is now cleanly saved as a string variable
cpu_name = fetch_cpu_name()


boot_time = time.time()

uptime = time.time() - boot_time

os_t = platform.system().lower(); gb = f"{round(psutil.virtual_memory().total / 1024**3, 2)} GB"
try:
    cmd = "wmic memorychip get speed" if "windows" in os_t else "sudo dmidecode --type 17 | grep 'Speed:'" if "linux" in os_t else "system_profiler SPMemoryDataType | grep 'Speed:'"
    out = subprocess.check_output(cmd, shell=True).decode()
    sp = [s.strip() if "windows" in os_t else s.split(":").strip() for s in out.split('\n') if (s.strip().isdigit() if "windows" in os_t else ":" in s and "Unknown" not in s)]
    speed = f"{', '.join(sp)} MHz" if sp else "Unknown"
except Exception: speed = "Unknown"

import platform
import subprocess
import re

def get_resolution():
    system = platform.system()

    if system == "Windows":
        import ctypes
        user32 = ctypes.windll.user32
        return f"{user32.GetSystemMetrics(0)}x{user32.GetSystemMetrics(1)}"

    elif system == "Linux":
        try:
            output = subprocess.check_output(
                ["xrandr"], text=True, stderr=subprocess.DEVNULL
            )
            match = re.search(r"(\d+)x(\d+)\+\d+\+\d+", output)
            if match:
                return f"{match.group(1)}x{match.group(2)}"
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

    elif system == "Darwin":
        try:
            output = subprocess.check_output(
                ["system_profiler", "SPDisplaysDataType"], text=True
            )
            match = re.search(r"Resolution:\s*(\d+)\s*x\s*(\d+)", output)
            if match:
                return f"{match.group(1)}x{match.group(2)}"
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

    return "Unknown"

resolution = get_resolution()

print(f"""
.....................   ..........
 :7J??7777777777777777??YPY?#BB#######J    OS: OpenTails 0.1 x86_64
75~.                     :?G?P~~@@7:^^:    Host: {host} {host_ver}
!G                          !P7P:&@^       Kernel: opentails-0.1-september-5-26
5?                           B^B~&@^       Shell: {shell}
!G                          ~P7P:&@^       Resolution: {resolution}
75~.                     :?G55.:@@^        CPU: {cpu_name}
75~.......................:?G?P:@@^        RAM: {gb} | Speed: {speed}

""")



while True:
    command = input("OpenTails> ")

    if command  == "exit":
        print("BYE!")
        break

    elif command == "sysinfo":
        print(f"""cpu": "{cpu_name}", "ram": "{gb}", "resolution": "{resolution}", "os": "{host} {host_ver}", "kernel": "opentails-0.1-september-3-26", "shell": "{shell}"}}""")

    elif command == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')

    elif command == "echo":
        print("Echoing...")
        args = input()
        print(args)

    elif command == "about":
        print(f"OpenTails Shell Version: {shell}")

    elif command == "cpu":
        print(cpu_name)

    elif command == "ram":
        print(gb)

    elif command == "resolution":
        print(resolution)

    elif command == "os":
        print(f"{host} {host_ver}")

    elif command == "resolution":
        print(resolution)

    elif command == "help":
        print("Available commands: sysinfo, clear, echo, about, cpu, ram, resolution, os, help, exit")

    else:
        print("Command Not Found.")
