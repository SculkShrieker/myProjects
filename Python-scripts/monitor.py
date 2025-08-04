import psutil
import subprocess
import time

SUSPICIOUS_COMMANDS = ['wget', 'curl', 'nc', 'python', 'bash', 'sh', 'base64']
ALERT_TRIGGERED = False

def check_tty_activity():
    for proc in psutil.process_iter(['pid', 'name', 'username', 'terminal', 'cmdline']):
        tty = proc.info['terminal']
        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
        if tty and tty.startswith('/dev/pts'):
            for keyword in SUSPICIOUS_COMMANDS:
                if keyword in cmdline:
                    return proc.info
    return None

def list_local_users():
    users = []
    with open("/etc/passwd", "r") as passwd_file:
        for line in passwd_file:
            fields = line.split(":")
            uid = int(fields[2])
            # Ignore system accounts (usually UID < 1000)
            if uid >= 1000:
                users.append(fields[0])
    return users

# Example usage
if __name__ == "__main__":
    print("🧑 Registered Local Users:")
    for user in list_local_users():
        print(f"  - {user}")



def shutdown_user(username):
    subprocess.call(['pkill', '-KILL', '-u', username])
    print(f"🔒 User {username} has been shut down for suspicious TTY activity.")

while True:
    result = check_tty_activity()
    if result and not ALERT_TRIGGERED:
        print("🚨 Alert: Suspicious TTY behavior detected")
        print(f"User: {result['username']}, Command: {' '.join(result['cmdline'])}")
        ALERT_TRIGGERED = True

        # Optional: log, send alert, write report
        shutdown_user(result['username'])  # Caution: This is a hard kill!

    time.sleep(5)
