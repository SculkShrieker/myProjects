import hmac
import hashlib
import base64

# ✅ Your target IP address
ip_to_check = "10.46.240.234"

# ✅ Hashed entries as (salt, hmac_val) pairs extracted from your known_hosts snippet
hashed_entries = [
    ("82247QpyO+6MJCIUnbecdX9Pz0Y=", "/J5KkntgmyOI1tDdza9JMSx5XTw="),
    ("1Dn5hNtUfPVZMEYyQLf0QYKkJus=", "A+s0p9edeP4kOSQKqPOLdakDOno="),
    ("nMTe/eR4rAZGMWAFevx5zPwoW78=", "MFj5atI2msazReY1bci+H7utR0c="),
    ("1GzTziFCBawZk7ql+kCEDElwgbs=", "cCBsHDGYnzGOhEMwMel8fURTULQ="),
    ("M2kASXmjoqpIjhgPs95+ftfJDH8=", "Yd27cuo0T1Ly6UExa0tWLYBun0I=")
]

def match_host(ip, salt_b64, hmac_b64):
    # Decode the salt and compute HMAC-SHA1
    salt = base64.b64decode(salt_b64)
    computed_hmac = hmac.new(salt, ip.encode(), hashlib.sha1).digest()
    computed_hmac_b64 = base64.b64encode(computed_hmac).decode()

    return computed_hmac_b64 == hmac_b64

# 🔍 Check each entry
for idx, (salt, hmac_val) in enumerate(hashed_entries, start=1):
    if match_host(ip_to_check, salt, hmac_val):
        print(f"[MATCH] Entry {idx} matches IP {ip_to_check}")
    else:
        print(f"\n[NO MATCH] Entry {idx} does NOT match")

