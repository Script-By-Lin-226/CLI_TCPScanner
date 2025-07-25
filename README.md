# 🔍 Advanced TCP Scanner

A powerful and flexible command-line tool to scan TCP ports, resolve domains, check host availability via ping, and sweep subnets. Logs all results in `.log` and `.json` formats with color-coded output and service detection.

---

## 🛠️ Features

- ✅ Scan a single IP or domain
- ✅ TCP port scanning with banner grabbing
- ✅ Detect if host is alive using `ping`
- ✅ Subnet sweep (`--swap`) to scan a full `/24` subnet
- ✅ Automatically detects common TCP services (HTTP, SSH, etc.)
- ✅ Color-coded output using `colorama`
- ✅ Logs activity to both `TCP_Scanner.log` and `log.json`

---

## ⚙️ Installation

1. Clone or download the project
2. Install the required library:

```bash
  pip install -r requirements
  pip install e . 
  scanTCP <Options>
  
  Arguments:
    --ip <IP> or --d <DOMAIN> [REQUIRED]
    --ports <ports> (add specific ports that you want to scan | if not it will go default [22,40,80,3306])
    --swap (Sweep ping 192.168.1.1 <- sweep from 1 to 255)
    
Example -> scanTCP --ip 192.168.1.1 --ports 21 22 23 80 443 --swap
    
    