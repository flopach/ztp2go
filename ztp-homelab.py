print ("\n\n *** Homelab Cat9300 | ZTP Day0 Python Script *** \n\n")

# Importing modules
from cli import configure, cli, pnp
import re
import json
import time

def get_model():
	try:
		show_version = cli('show version')
	except pnp._pnp.PnPSocketError:
		time.sleep(90)
		show_version = cli('show version')
	try:
		serial = re.search(r"Model Number\s+:\s+(\S+)", show_version).group(1)
	except AttributeError:
		serial = re.search(r"Processor board ID\s+(\S+)", show_version).group(1)
	return serial

def main():
	model = get_model()
	print ('*** Model Number: %s ***' % model)

	import cli

	cli.configurep(["license boot level network-advantage addon dna-advantage"])

	cli.configurep(["ip routing"])
	cli.configurep(["ip domain name cisco.com"])

	cli.configurep(["interface loopback 0", "ip address 192.168.178.111 255.255.255.0", "end"])


	cli.configurep(["int vlan 1", "ip address 192.168.178.110 255.255.255.0", "no shut", "end"])
	cli.configurep(["ip default-gateway 192.168.178.1", "end"])

	cli.configurep(["username cisco privilege 15 secret cisco"])

	cli.configurep(["snmp-server community Public RO "])
	cli.configurep(["snmp-server community Private RW "])

	cli.configurep(["ip ssh source-interface Loopback0"])
	cli.configurep(["ip ssh version 2"])

	cli.configurep(["aaa new-model", "aaa authentication login default local", "end"])
	cli.configurep(["aaa authorization exec default local", "aaa session-id common", "end"])

	cli.configurep(["line con 0" , "privilege level 15" , "stopbits 1", "end"])
	cli.configurep(["line vty 0 15" , "privilege level 15" , "login local", "transport input all", "end"])

	cli.configurep(["hostname {}".format(model)])
	cli.configurep(["netconf-yang", "end"])

	print ("\n\n *** Executing show ip interface brief  *** \n\n")
	cli_command = "sh ip int brief"
	cli.executep(cli_command)

	print ("\n\n *** Homelab Cat9300 | ZTP Day0 Python Script Execution Complete *** \n\n")


if __name__ in "__main__":
	main()
