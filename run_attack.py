#!/usr/bin/env python3
import argparse
from dos.dos import Dos
from portscanning.portscanning import PortScanning
from netmapping.netmapping import NetworkMapping
from privesc.hostexec import HostWrite
from ssltls.ssltls import SSLTLSAttack


parser = argparse.ArgumentParser(
    prog="5G-core Attackset attack generator",
    description="A script that executes and logs the variety of the attacks that are in-scope for the 5G core attackset.")

parser.add_argument("type")

args = parser.parse_args()

attack = None

if args.type == "port_scanning":
    attack = PortScanning("10.110.198.65")
if args.type == "denial_of_service":
    attack = Dos()
if args.type == "net_mapping":
    attack = NetworkMapping("10.110.198.65")
if args.type == "ssl_tls":
    attack = SSLTLSAttack("10.110.198.65" ,"255.255.255.0")
if args.type == "host_exec":
    attack = HostWrite()
if attack is None:
    raise ValueError("Invalid Argument")


attack.get_log_start()
attack.execute()
attack.get_log_end()
