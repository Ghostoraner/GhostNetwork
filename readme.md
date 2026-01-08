
# GhostNetwork 🛡️💻

**GhostNetwork** is a powerful, modular network analysis and system monitoring toolkit designed specifically for UNIX-like operating systems (Arch Linux, Debian, macOS, etc.). It merges the capabilities of professional security utilities with a modern, high-performance Graphical User Interface (GUI) built on CustomTkinter.

---

## 🚀 Key Features
- **ARP Network Discovery**: Real-time identification of active devices within your local network.
- **Deep Port Scanning**: Identify service versions and open ports using the Nmap engine.
- **Web Vulnerability Audit**: Scan for server misconfigurations and hidden vulnerabilities using Nikto.
- **IP Intelligence**: One-click geolocation lookup (Country, City, ISP) and Public IP verification.
- **Unix System Stats**: Instant monitoring of CPU Load Average and RAM utilization.
- **Reporting System**: Save terminal outputs directly into organized .txt reports for documentation.

---

## 🛠️ System Prerequisites

GhostNetwork acts as a bridge for industry-standard tools. You must install these dependencies on your host system:

### Arch Linux:
```bash
sudo pacman -S nmap nikto dirb whois bind-tools procps-ng
```
### Debian / Ubuntu:
```bash
sudo apt update && sudo apt install nmap nikto dirb whois dnsutils procps
```

---

## 📦 Installation & Usage

```bash
git clone https://github.com/Ghostoraner/GhostNetwork.git
cd GhostNetwork
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo python main.py
```

---

## 📁 Project Architecture 
```
GhostNetwork/
├── main.py # Launch GUI
├── requirements.txt # Dependencies
├── README.md # Updated documentation
└── core/
       ├── __init__.py
       ├── scanner.py # Logic (ARP + Port Scan)
       └── styles.py # GUI color settings
```

---


## ✅ Conclusion
- Author: Ghostoraner
- Сommunication: reinsss21@gmail.com

---

© 2026 Ghostoraner  
Released under the MIT License.
