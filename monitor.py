import csv
import time
import subprocess
import sqlite3
from datetime import datetime
import platform
import subprocess

DB_NAME = 'db.sqlite3'

def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    host TEXT,
                    status TEXT,
                    latency REAL,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

def ping(host):
    system = platform.system().lower()

    if system == 'windows':
        command = ['ping', '-n', '1', '-w', '1000', host]
    else:
        command = ['ping', '-c', '1', '-W', '1', host]

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)

        # Try to extract latency from any line with "time=" (case-insensitive)
        for line in output.splitlines():
            if "time=" in line.lower():
                latency_str = line.lower().split("time=")[-1].split()[0].replace("ms", "")
                return "Online", float(latency_str)
        return "Online", None  # If latency parsing fails, still mark as Online
    except subprocess.CalledProcessError:
        return "Offline", None

def monitor():
    with open('targets.csv', 'r') as f:
        reader = csv.DictReader(f)
        targets = list(reader)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for target in targets:
        name, host = target['name'], target['host']
        status, latency = ping(host)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO results (name, host, status, latency, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (name, host, status, latency, timestamp))
        print(f"{timestamp} - {name} ({host}) is {status} - {latency} ms")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    while True:
        monitor()
        time.sleep(60)  # Monitor every 60 seconds
