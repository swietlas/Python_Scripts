#!/usr/bin/env python3
from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_scrapli.functions import print_structured_result
from nornir_utils.plugins.functions import print_result
import ipdb
from rich import print as rprint


nr = InitNornir(config_file="config_vios.yaml")

def sh_command_task (task):
    int_brief_result = task.run(task=send_command, command="show ip interface brief")
    #version_result = task.run(task=send_command, command="show version")
    #task.host["facts"] = version_result.scrapli_response.genie_parse_output()
    
    task.host["facts"] = int_brief_result.scrapli_response.genie_parse_output()
    interfaces =  task.host["facts"]["interface"]
    #for host in task.host:
    for intf in interfaces:
        ipaddr = interfaces[intf]["ip_address"]
        status = interfaces[intf]["status"]
        if ipaddr != "unassigned":
            rprint(f"{task.host} [green]Interface {intf} is {status} and has {ipaddr}[/green]  \n ")
        else: 
            rprint  (f"{task.host} [red]Interface {intf} is unassigned[/red]  \n")  
    #eth0 = taks.host["facts"][interface]
   # print(f"{task.host} has interface 1 {eth0}" )

result = nr.run(sh_command_task)
#print_structured_result(result, parser="genie")
print_result(result)

# ipdb.set_trace()

# ipdb> nr.inventory.hosts["R1"]["facts"]
# {'interface': {'Ethernet0/0': {'ip_address': '64.100.0.2', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'up', 'protocol': 'up'}, 'Ethernet0/1': {'ip_address': '10.10.0.1', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'up', 'protocol': 'up'}, 'Ethernet0/2': {'ip_address': 'unassigned', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'administratively down', 'protocol': 'down'}, 'Ethernet0/3': {'ip_address': '10.10.7.110', 'interface_is_ok': 'YES', 'method': 'DHCP', 'status': 'up', 'protocol': 'up'}, 'Tunnel1': {'ip_address': '172.16.1.1', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'up', 'protocol': 'up'}}}
# ipdb> nr.inventory.hosts["R1"]["facts"][interface]
# *** NameError: name 'interface' is not defined
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"]
# {'Ethernet0/0': {'ip_address': '64.100.0.2', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'up', 'protocol': 'up'}, 'Ethernet0/1': {'ip_address': '10.10.0.1', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'up', 'protocol': 'up'}, 'Ethernet0/2': {'ip_address': 'unassigned', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'administratively down', 'protocol': 'down'}, 'Ethernet0/3': {'ip_address': '10.10.7.110', 'interface_is_ok': 'YES', 'method': 'DHCP', 'status': 'up', 'protocol': 'up'}, 'Tunnel1': {'ip_address': '172.16.1.1', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'up', 'protocol': 'up'}}
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"][1]
# *** KeyError: 1
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"]['1']
# *** KeyError: '1'
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"]["Ethernet0/0"]
# {'ip_address': '64.100.0.2', 'interface_is_ok': 'YES', 'method': 'NVRAM', 'status': 'up', 'protocol': 'up'}
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"]["Ethernet0/0"].ip_address
# *** AttributeError: 'dict' object has no attribute 'ip_address'
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"]["Ethernet0/0"]["ip_address"]
# '64.100.0.2'
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"]["Ethernet0/0"]["status"]
# 'up'
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"]["Ethernet0/0"]["protocol"]
# 'up'
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"]["Ethernet0/2"]["protocol"]
# 'down'
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"]["Ethernet0/2"]["status"]
# 'administratively down'
# ipdb> nr.inventory.hosts["R1"]["facts"]["interface"]["Ethernet0/2"]["ip_address"]
# 'unassigned'
