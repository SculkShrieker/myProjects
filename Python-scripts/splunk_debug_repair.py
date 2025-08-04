import os
import subprocess
from pathlib import Path

# Constants
splunk_bin_path = "/opt/splunk/bin"
bashrc_path = Path.home() / ".bashrc"
splunk_cmd = f"{splunk_bin_path}/splunk"
script_path = f"{splunk_bin_path}/scripts/stop_bettercap.sh"
launch_conf_path = "/opt/splunk/etc/splunk-launch.conf"

def splunk_exists():
    return Path(splunk_cmd).exists()

def add_to_path():
    export_cmd = f'export PATH=$PATH:{splunk_bin_path}\n'
    if not bashrc_path.read_text().count(splunk_bin_path):
        with open(bashrc_path, 'a') as file:
            file.write(export_cmd)
        print("[+] Added Splunk bin to PATH in .bashrc")
        subprocess.run(["bash", "-c", "source ~/.bashrc"])

def validate_alert_action():
    try:
        result = subprocess.run([splunk_cmd, "btool", "alert_actions", "list", "stop_bettercap", "--debug"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("[+] Btool output:\n", result.stdout)
        if result.stderr:
            print("[!] Btool errors:\n", result.stderr)
    except Exception as e:
        print("[!] Error validating alert action:", e)

def make_script_executable():
    if Path(script_path).exists():
        os.chmod(script_path, 0o755)
        print(f"[+] Script '{script_path}' made executable.")
    else:
        print(f"[!] Script '{script_path}' not found.")

def set_https_verify():
    try:
        with open(launch_conf_path, 'a') as file:
            file.write('\nPYTHONHTTPSVERIFY=1\n')
        print("[+] PYTHONHTTPSVERIFY set to 1 for secure Python requests.")
    except Exception as e:
        print(f"[!] Failed to update {launch_conf_path}: {e}")

def main():
    if not splunk_exists():
        print("[!] Splunk CLI not found at expected location.")
        return
    print("[*] Splunk CLI found.")
    add_to_path()
    make_script_executable()
    validate_alert_action()
    set_https_verify()
    print("[✔] Environment cleanup and validation complete.")

if __name__ == "__main__":
    main()
