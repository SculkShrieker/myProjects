import subprocess

def run_nmap(target, scan_type="basic"):
    scans = {
    "basic": ["-sV", "-O"],
    "aggressive": ["-A"],
    "ping": ["-sn"],
    "quick": ["-T4", "-F"],
    "quiet": ["-T0", "-n", "-Pn", "-sS", "--data-length", "50"],  # <- quiet scan
    "full": ["-p-", "-sV", "-O"],  # <- don't forget the comma above!
    "full & quick": ["-p-", "-sV", "-O", "-T4"], #make sure all the expressions are correct!

}


    if scan_type not in scans:
        print(f"Unsupported scan type: {scan_type}")
        return

    nmap_cmd = ["nmap"] + scans[scan_type] + [target]
    print(f"\n🔍 Executing: {' '.join(nmap_cmd)}\n")
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"⚠️ Error: {result.stderr}")

# 🌐 Trigger-based interface
def main():
    print("👋 Welcome to Nmap Recon Assistant.")
    target_ip = input("🎯 Enter target IP: ")

    while True:
        command = input("\n🗨️ Type a phrase (e.g., 'Scan', 'Scan aggressive', 'Scan full', 'Scan quick', 'Scan quiet', 'Exit'): ").strip().lower()

        if command == "exit":
            print("👋 Exiting script.")
            break
        elif command.startswith("scan"):
            parts = command.split()
            scan_type = parts[1] if len(parts) > 1 else "basic"
            run_nmap(target_ip, scan_type)
        else:
            print("🤔 Unrecognized command. Try phrases like 'Scan', 'Scan aggressive', or 'Exit'.")

if __name__ == "__main__":
    main()
