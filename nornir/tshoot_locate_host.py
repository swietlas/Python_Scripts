#!/usr/bin/env python3

from netmiko import ConnectHandler
import pprint
import ipdb
from scrapli.driver.core import IOSXEDriver

target_host="192.168.40.10"
R1v = "10.10.7.215"

print("Connecting to fist hope RTR and sending traceroute to find final router")
#scrapli
# device1 = {
#     "host": R1v,
#     "auth_username": "ansi",
#     "auth_password": "C1sc0123!",
#     "auth_strict_key": False,
# }

# Netmiko
device1 = {
    'device_type': 'cisco_ios',
    'ip': 'R1v',
    'username': 'ansi',
    'password': 'C1sc0123!',
}
pp = pprint.PrettyPrinter(indent=4)

# conn = IOSXEDriver(**device1)
# conn.open()
# netmiko
net_connect = ConnectHandler(**device1)
output_ping = net_connect.send_command(f"ping {target_host}")
output_traceroute = net_connect.send_command(f"traceroute {target_host}", use_textfsm=True)
#scrapli
#output = conn.send_command(f"traceroute {target_host}")
target_rtr = output_traceroute[-2]['address']
pp.pprint(output)

print(f"\nTarget router is {target_rtr}")
#ipdb.set_trace()


device2 = {
    'device_type': 'cisco_ios',
    #'ip': target_rtr,
    'ip': 'R4v',
    'username': 'ansi',
    'password': 'C1sc0123!',
}
net_connect = ConnectHandler(**device2)
output_arp = net_connect.send_command('show arp 192.168.40.10', use_genie=True)
print(output_arp)
#output_neigh= net_connect.send_command('show arp 192.168.40.10', use_textfsm=True)
ipdb.set_trace()