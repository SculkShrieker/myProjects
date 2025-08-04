import psutil
import subprocess
import time
import datetime
import platform
import re


# ⚙️ Config
SUSPICIOUS_COMMANDS = ['wget', 'curl', 'nc', 'python3', 'bash', 'sh', 'base64', 'nmap', 'killall']
EXCLUDED_USERS = ['admin', 'backupbot', 'sculk']
LOG_FILE = "tty_monitor.log"
ALERT_TRIGGERED = False

def is_suspicious(cmdline):
    pattern = r'\b(' + '|'.join(SUSPICIOUS_COMMANDS) + r')\b'
    return bool(re.search(pattern, cmdline))



def debug_thinlinc_processes(users):
    for proc in psutil.process_iter(['pid', 'username', 'cmdline']):
        if proc.info['username'] in users:
            log_event(f"🔍 ThinLinc trace — User: {proc.info['username']}, PID: {proc.info['pid']}, CMD: {' '.join(proc.info['cmdline'])}")

# 📝 Logging function
def log_event(message):
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}\n"
    with open(LOG_FILE, "a") as logfile:
        logfile.write(entry)
    print(entry.strip())

# 🔔 Notification handler
def cross_notify(title, message):
    system_type = platform.system()
    if system_type == "Linux":
        try:
            subprocess.call(['notify-send', title, message])
        except FileNotFoundError:
            print("🛑 GNOME notify-send not found.")
    elif system_type == "Windows":
        import winsound
        winsound.Beep(1000, 500)
        print(f"🔔 Windows alert: {title} — {message}")
    else:
        print(f"🔔 [Generic Notification] {title}: {message}")

# 👥 Local user enumerator
def list_local_users():
    users = []
    with open("/etc/passwd", "r") as passwd_file:
        for line in passwd_file:
            fields = line.split(":")
            uid = int(fields[2])
            if uid >= 1000:
                users.append(fields[0])
    return users

# 🛠️ Session controls
def sleep_user_session(username):
    subprocess.call(['pkill', '-STOP', '-u', username])
    log_event(f"😴 User {username}'s session was paused.")

def shutdown_user_session(username):
    subprocess.call(['pkill', '-KILL', '-u', username])
    log_event(f"🔒 User {username} was forcibly shut down.")

def send_user_alert(username, command):
    log_event(f"📣 Simulated alert sent to {username} for command: {command}")

# 🚨 Escalation handler
def escalation_menu(username, command):
    cross_notify("🚨 TTY Monitor Alert", f"Suspicious activity by {username}: {command}")
    log_event(f"🚨 Suspicious activity detected → User: {username}, Command: {command}")

    print("\n⚠️ Escalation Options:")
    print("  1. Sleep detected user")
    print("  2. Shutdown detected user")
    print("  3. Send alert message to user")
    print("  4. Ignore and continue monitoring")

    choice = input("🔧 Your choice (1-4): ").strip()
    if choice == "1":
        sleep_user_session(username)
    elif choice == "2":
        shutdown_user_session(username)
    elif choice == "3":
        send_user_alert(username, command)
    else:
        log_event("🕊️ No action taken.")

# 🔍 TTY process detector
def check_tty_activity(local_users):
    for proc in psutil.process_iter(['pid', 'name', 'username', 'terminal', 'cmdline']):
        tty = proc.info['terminal']
        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
        user = proc.info['username']

        if tty and tty.startswith('/dev/pts'):
            matched_command = any(keyword in cmdline for keyword in SUSPICIOUS_COMMANDS)
            excluded_user = user in EXCLUDED_USERS
            matched_user = user in local_users and not excluded_user

            if matched_command and matched_user:
                log_event(f"🚨 TTY alert: {user} ran suspicious command: {cmdline}")
                escalation_menu(user, cmdline)
            elif excluded_user:
                log_event(f"🛡️ Skipped excluded TTY user={user}, Command: {cmdline}")
            elif user in local_users:
                log_event(f"❌ Benign TTY command by local user={user}: {cmdline}")
            else:
                log_event(f"❌ TTY command by non-local user={user}: {cmdline}")

# 🔍 ThinLinc session tracker
def get_thinlinc_users():
    active_users = set()
    for proc in psutil.process_iter(['pid', 'username', 'name', 'cmdline']):
        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
        if any(tag in cmdline for tag in ['tlclient', 'tlwebaccess', 'vncserver', 'Xvnc']):
            active_users.add(proc.info['username'])
    return list(active_users)

def scan_thinlinc_user_commands(thinlinc_users, local_users):
    for proc in psutil.process_iter(['pid', 'username', 'cmdline']):
        user = proc.info['username']
        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
        if user in thinlinc_users:
            matched_command = any(keyword in cmdline for keyword in SUSPICIOUS_COMMANDS)
            excluded_user = user in EXCLUDED_USERS
            matched_user = user in local_users and not excluded_user

            if matched_command and matched_user:
                log_event(f"🚨 ThinLinc alert: {user} ran suspicious command: {cmdline}")
                escalation_menu(user, cmdline)
            elif excluded_user:
                log_event(f"🛡️ Skipped excluded ThinLinc user={user}, Command: {cmdline}")
            elif user in local_users:
                log_event(f"❌ Benign ThinLinc command by local user={user}: {cmdline}")
            else:
                log_event(f"❌ ThinLinc command by non-local user={user}: {cmdline}")

# 🧠 Main loop
if __name__ == "__main__":
    print("🧑 Registered Local Users:")
    local_users = list_local_users()
    for user in local_users:
        print(f"  - {user}")
    print(f"📄 Logging to: {LOG_FILE}\n")

    while True:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

        # Monitor TTY
        check_tty_activity(local_users)

        # Monitor ThinLinc
        thinlinc_users = get_thinlinc_users()
        if thinlinc_users:
            scan_thinlinc_user_commands(thinlinc_users, local_users)
        else:
            log_event(f"{timestamp} 📡 No ThinLinc activity detected")

        time.sleep(10)
