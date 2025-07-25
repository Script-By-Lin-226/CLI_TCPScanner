import platform
import socket
import subprocess
import datetime
import json
import argparse
import logging
from colorama import Fore, init

# ----------------
# Logger
# ----------------
init(autoreset=True)
logger = logging.getLogger('TCP_Scanner')
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
fileHandler = logging.FileHandler('TCP_Scanner.log')
formatter = logging.Formatter('( %(asctime)s ) - %(name)s - %(levelname)s - %(message)s | %(filename)s::%(funcName)s::%(lineno)d')

console.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(fileHandler)

# ----------------
# Parse CLI
# ----------------
def cli_argparse():
    parser = argparse.ArgumentParser(description='Advanced TCP Scanner')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--d', help='Target domain')
    group.add_argument('--ip', help='Target IP address')
    parser.add_argument('--ports', type=int, nargs='*', help='Target port list')
    parser.add_argument('--swap', action='store_true', help='Enable subnet sweep')
    return parser.parse_args()

# ----------------
# Utilities

def is_alive(ip):
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        res = subprocess.getoutput(f'ping {param} 1 {ip}')
        return 'ttl' in res.lower()
    except Exception:
        logger.exception(f'Ping failed for {ip}')
        return False

def convert_domain(domain):
    try:
        ip = socket.gethostbyname(domain)
        if is_alive(ip):
            logger.info(f'Target domain {domain} resolved to {ip} and is alive.')
            return ip
        else:
            logger.warning(f'Target domain {domain} resolved to {ip}, but is dead.')
            return None
    except Exception:
        logger.exception(f'Domain resolution failed: {domain}')
        return None

# ----------------
# Core Functions
# ----------------
def port_scanner(ip, ports, result_list=None):
    for port in ports:
        banner = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            try:
                service = socket.getservbyport(port,'tcp')
            except OSError:
                service = None

            if result == 0:
                try:
                    s.settimeout(1)
                    banner = s.recv(1024).decode(errors='ignore').strip()
                except Exception:
                    banner = 'No banner or unreadable'
                msg = f'[+] Port {port} is open at {ip}'
                logger.info(msg)
                print(Fore.GREEN + msg)
                status = 'Open'
            else:
                msg = f'[-] Port {port} is closed at {ip}'
                logger.info(msg)
                print(Fore.RED + msg)
                status = 'Closed'


            if result_list is not None:
                result_list.append({
                    'ip': ip,
                    'port': port,
                    'status': status,
                    'service': service,
                    'Banner': banner if status == 'Open' else None,
                    'timestamp': datetime.datetime.now().isoformat()
                })

            s.close()
        except Exception as e:
            logger.exception(f'Error scanning port {port} on {ip}')

def swap_ip(base_ip, ports, result_list=None):
    for i in range(1, 255):
        current_ip = f'{base_ip}.{i}'
        if is_alive(current_ip):
            logger.info(f'IP {current_ip} is alive. Scanning...')
            port_scanner(current_ip, ports, result_list)
        else:
            logger.warning(f'IP {current_ip} is unreachable.')

# ----------------
# Main
# ----------------
def main():
    args = cli_argparse()
    ports = args.ports if args.ports else [22, 40, 80, 3306]
    result_list = []

    if args.d:
        target_ip = convert_domain(args.d)
        if not target_ip:
            print(Fore.RED + f'[!] Domain "{args.d}" could not be resolved or is unreachable.')
            return
    else:
        if len(args.ip.split('.')) != 4:
            print(Fore.RED + '[!] Invalid IPv4 address.')
            return
        target_ip = args.ip

    if args.swap:
        base_ip = '.'.join(target_ip.split('.')[:-1])
        logger.info(f'Starting subnet sweep on {base_ip}.x')
        swap_ip(base_ip, ports, result_list)
    else:
        port_scanner(target_ip, ports, result_list)

    try:
        with open('log.json', 'w') as f:
            json.dump(result_list, f, indent=4)
            print(Fore.CYAN + '[+] Results saved to log.json')
    except Exception as e:
        logger.exception(f'Error saving results to log.json: {e}')
        print(Fore.RED + f'[!] Error saving results to log.json: {e}')


if __name__ == '__main__':
    main()