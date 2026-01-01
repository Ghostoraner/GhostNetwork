from scapy.all import ARP, Ether, srp
import socket


class NetworkScanner:
    @staticmethod
    def scan_network(ip_range):
        """ARP сканування для пошуку пристроїв."""
        try:
            arp = ARP(pdst=ip_range)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            result = srp(ether / arp, timeout=2, verbose=False)[0]

            devices = []
            for _, received in result:
                devices.append({'ip': received.psrc, 'mac': received.hwsrc})
            return devices
        except Exception as e:
            return str(e)

    @staticmethod
    def check_port(ip, port):
        """Швидка перевірка одного порту."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            return s.connect_ex((ip, port)) == 0