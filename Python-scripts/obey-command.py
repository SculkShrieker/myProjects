from flask import Flask, request
import subprocess
import os

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_command():
    data = request.json
    cmd = data.get("command")

    if not cmd:
        return {"status": "error", "message": "No command provided"}, 400

    try:
        # Assumes GUI session is DISPLAY=:0 and access is allowed
        result = subprocess.run(cmd, shell=True, env={"DISPLAY": ":0"}, capture_output=True, text=True)
        return {"status": "success", "output": result.stdout}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

