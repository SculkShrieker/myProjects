Before using the scripts in this repository, ensure your system has the necessary Python environment and dependencies installed. These steps are designed for Ubuntu 20.04+ and other Debian-based distributions. However, functionality on other Linux systems may vary outside Debian based distributions

1. Ubuntu may come with Python pre-installed, but it's best to confirm the version:
   python3 --version
   If your version is below 3.10, install the latest with:
   sudo apt update
   sudo apt install python3.10 python3.10-venv python3.10-dev

2. Ensure pip Is Installed and Updated: 
   sudo apt install python3-pip
   python3 -m pip install --upgrade pip


3. Use a Virtual Environment:
   python3 -m venv .venv
   source .venv/bin/activate

4. Install Dependencies Manually, e.g :
   pip install psutil requests splunk-sdk
   Or if you have the requirements.txt, you can run:
   pip install -r requirements.txt

5. You can now run your python script inside the terminal: (e.g  python3 script_name.py)
   You can also include your full path to your script to ensure it's working in case you're not in the current script's directory (e.g python3 /your/path/to/script/script_name.py or /usr/bin/python3 /your/path/to/script/script_name.py   

6. 🔐 Permissions Note ⚠️:

   Some scripts (like those controlling services) may require root privileges to operate (sudo). Make sure you have the required privileges, or run the script with:
   sudo python3 script_name.py

      


 
 

 
