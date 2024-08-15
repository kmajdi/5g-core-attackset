from privesc.hostexec import HostWrite
from ssltls.ssltls import SSLTLSAttack
from netmapping.netmapping import NetworkMapping
from portscanning.portscanning import PortScanning
from dos.dos import Dos

attack_dict = {"port_scanning": PortScanning,
               "denial_of_service": Dos,
               "net_mapping": NetworkMapping,
               "ssl_tls": SSLTLSAttack,
               "host_exec": HostWrite}

def get_attack(attack_type):
    return attack_dict[attack_type]()

