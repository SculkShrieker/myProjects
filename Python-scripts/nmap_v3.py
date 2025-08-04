import subprocess

# Define Nmap scan profiles
SCAN_TYPES = {
    "basic": ["-sV", "-O"],
    "aggressive": ["-A"],
    "ping": ["-sn"],
    "quick": ["-T4", "-F"],
    "quiet": ["-T0", "-n", "-Pn", "-sS", "--data-length", "50"],
    "full": ["-p-", "-sV", "-O"],
    "ports": ["-p-", "--open"]  # ✅ Fixed comma added
}

def build_scan_flags(scan_input):
    # Handle combined scan types like "full & quick & aggressive"
    scan_types = [part.strip() for part in scan_input.split("&")]
    flags = []
    for scan in scan_types:
        if scan not in SCAN_TYPES:
            print(f"⚠️ Unsupported scan type: {scan}")
        else:
            flags.extend(SCAN_TYPES[scan])
    # Remove duplicates while preserving order
    seen = set()
    deduped_flags = [f for f in flags if not (f in seen or seen.add(f))]
    return deduped_flags

def run_nmap(target, scan_combo="basic"):
    scan_flags = build_scan_flags(scan_combo)
    if not scan_flags:
        print("❌ No valid scan types provided.")
        return

    nmap_cmd = ["nmap"] + scan_flags + [target]
    print(f"\n🔍 Executing: {' '.join(nmap_cmd)}\n")
    result = subprocess.run(nmap_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"⚠️ Error: {result.stderr}")

def main():
    print("👋 Welcome to Nmap Recon Assistant.")
    
    while True:
        target_ip = input("🎯 Enter target IP (or type 'exit' to quit): ").strip()
        if target_ip.lower() == "exit":
            print("👋 Exiting script.")
            return

        # Enter scanning loop
        while True:
            print("\n🗨️ Available scan types:")
            print("  - basic, aggressive, full, quick, quiet, ping, ports")
            print("  - Combine with '&' (e.g., 'full & quick & aggressive')")
            print("  - Type 'back' to re-enter IP or 'exit' to quit")

            command = input("🔎 Enter scan command: ").strip().lower()

            if command == "exit":
                print("👋 Exiting script.")
                return
            elif command == "back":
                break
            elif command.startswith("scan"):
                scan_combo = command.replace("scan", "").strip()
                scan_combo = scan_combo or "basic"
                run_nmap(target_ip, scan_combo)
            else:
                print("🤔 Unrecognized command. Use 'scan [type]' or 'scan [type & type]'. Example: scan full & ports")

if __name__ == "__main__":
    main()
