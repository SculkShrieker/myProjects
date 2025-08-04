import hmac
import hashlib
import base64

ip_to_hosts = ["10.46.234.240, 192.168.136.234, 192.168.76.234, 192.168.132.234, 192.168.136.235"]

def match_host(ip_to_hosts, salt_b64, hmac_b64):
    # Decode the salt from base64
    salt = base64.b64decode(salt_b64)
    
    # Create HMAC-SHA1 using the salt aas key and the IP as message
    computed_hmac = hmac.new(salt, ip_to_hosts.encode(), hashlib.sha1).digest()
    
    # Encode the result to base64
    computed_hmac_b64 = base64.b64encode(computed_hmac).decode()
    
    # Compare with stored HMAC
    return computed_hmac_b64 == hmac_b64

# Example usage
ip = "192.168.136.234"
salt = "1Dn5hNtUfPVZMEYyQLf0QYKkJus="   # replace with salt from known_hosts entry
hmac_val = "A+s0p9edeP4kOSQKqPOLdakDOno="  # replace with HMAC from known_hosts entry




if match_host(ip, salt, hmac_val):
    print(f"{ip} matches the hashed entry")
else:
    print(f"{ip} does NOT match, trying other IPs...")
    for host_ip in ip_to_hosts:
        if match_host(host_ip, salt, hmac_val):
            print(f"{host_ip} matches the hashed entry")
            break
    else:
        print("No IPs matched the hashed entry.")

