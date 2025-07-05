# Network-fault-monitor
# 🛰️ Automated Network Fault Monitor

A Linux-based network monitoring tool built with **Python**, **Flask**, and **SQLite**. This tool allows you to:

- Upload a list of IP addresses/hosts from a CSV file.
- Ping them every minute.
- Record status (Online/Offline), latency, and timestamp.
- View the results on a clean web dashboard.

---

## 📷 Preview

![screenshot](https://drive.google.com/file/d/1Vij6N6zCak4eXAcpDHE2ZuI7vUC83ZIm/view?usp=sharing)


---

## 🧰 Tech Stack

- Python 3
- Flask
- SQLite3
- HTML + CSS (Jinja2 templates)
- Linux Ping (subprocess)

---

## 📁 Project Structure

network_fault_monitor/

├── app.py # Flask web server

├── monitor.py # Ping monitor script

├── targets.csv # List of hosts to monitor

├── db.sqlite3 # Auto-created SQLite database

├── templates/

│ └── dashboard.html # Jinja2 HTML dashboard
├── static/

│ └── style.css # Dashboard styling


---

## 🚀 Setup & Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/laduta/network_fault_monitor.git
cd network_fault_monitor

### 2. Install dependencies
```bash
pip install flask

### 3. Add your targets
```bash
Edit targets.csv:
name,host
Google,8.8.8.8
Cloudflare,1.1.1.1
OpenDNS,208.67.222.222

### 3. Start monitoring (in background)
```bash 
python3 monitor.py

### 5. Launch web dashboard (in a new terminal)
```bash 
python3 app.py

Then open your browser: http://localhost:5000














