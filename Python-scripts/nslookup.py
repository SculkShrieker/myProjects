import socket
import dns.resolver
from datetime import datetime

def sanitize_domain(url):
    # Remove URL scheme and path
    if "://" in url:
        url = url.split("://")[1]
    return url.split("/")[0]

def get_records(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        return [rdata.to_text() for rdata in answers]
    except Exception as e:
        return [f"Error resolving {record_type}: {e}"]

def dns_scan(domain):
    domain = sanitize_domain(domain)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n📡 DNS Scan for {domain} — {timestamp}")
    print("-" * 60)

    records = {
        "A": [],
        "NS": [],
        "MX": [],
        "SOA": [],
        "TXT": []
    }

    # A Record using socket (fallback)
    try:
        ip = socket.gethostbyname(domain)
        records["A"].append(ip)
    except Exception as e:
        records["A"].append(f"Socket error: {e}")

    # Other records via dnspython
    for rtype in ["NS", "MX", "SOA", "TXT"]:
        records[rtype] = get_records(domain, rtype)

    # Print results
    for rtype, values in records.items():
        print(f"\n[{rtype}] Records:")
        for val in values:
            print(f"  - {val}")

    print("-" * 60)

# Entry point
if __name__ == "__main__":
    target = input("🔍 Enter a domain or URL: ").strip().lower()
    dns_scan(target)
