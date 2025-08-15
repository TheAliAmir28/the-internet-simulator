# 🌐 The Internet Simulator

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

## 📌 Overview
**The Internet Simulator** is a **CLI-based Python application** that mimics core networking operations.  
It lets you create servers, connect them, and perform commands like `ping`, `traceroute`, and `ip-config` — just like you would on a real network.

---

## 🚀 Features
✅ Create servers with **unique names** and **valid IPv4 addresses**  
✅ Establish **bi-directional connections** between servers with latency times  
✅ Select a **current server** to execute commands from  
✅ Use **ping** to check connectivity and latency  
✅ Perform **traceroute** to see the full network path  
✅ View **IP configuration** of the selected server  
✅ Display the **full server list** and their connections  

---

## 📂 Project Structure
```
the_internet.py   # Main program file
```

---

## 🛠️ Installation & Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/the-internet-simulator.git
   cd the-internet-simulator
   ```

2. **Run the program**
   ```bash
   python3 the_internet.py
   ```

---

## 📖 Usage Examples
Example session:
```bash
>>> create-server server1 192.168.0.1
Success: A server with name server1 was created at ip 192.168.0.1

>>> create-server server2 192.168.0.2
Success: A server with name server2 was created at ip 192.168.0.2

>>> create-connection server1 server2 15
Success: A server with the name server1 is now connected to server2

>>> set-server server1
Server server1 selected.

>>> ping server2
Reply from server1 time = 15 ms.

>>> traceroute server2
Tracing route to server2:
0  0  [192.168.0.1]  server1
1  15  [192.168.0.2]  server2
Trace complete.
```

---

## 📜 Command Reference
| Command | Description | Example |
|---------|-------------|---------|
| `create-server [name] [ip]` | Creates a new server | `create-server server1 192.168.0.1` |
| `create-connection [server1] [server2] [time]` | Connects two servers with latency time (ms) | `create-connection server1 server2 10` |
| `set-server [name/ip]` | Selects a server for operations | `set-server server1` |
| `ping [name/ip]` | Checks reachability & latency | `ping server2` |
| `traceroute [name/ip]` | Shows network path & times | `traceroute server3` |
| `ip-config` | Displays selected server’s name & IP | `ip-config` |
| `display-servers` | Lists all servers & their connections | `display-servers` |
| `quit` | Exits the program | `quit` |

---

## ⚙️ Requirements
- Python **3.x**
- No external libraries required

---

## 📄 License
This project is licensed under the **MIT License** — you’re free to use, modify, and share it.

---

## 👨‍💻 Author
**Ali Amir**  
📧 a476@umbc.edu
