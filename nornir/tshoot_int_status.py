#!/usr/bin/env python3
"""
Crated by: swietlas

This is script retrieves and processes interface status from Cisco network devices

Don't forget to install scrapli, norninr_scrapli, nornir utils, textfsm and genie
pip install nornir scrapli

pip install nornir
pip install ipdb
pip install rich
pip install scrapli[genie]
pip install nornir
pip install nornir-scrapli
pip install nornir_utils

"""


from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.functions import print_structured_result
import ipdb
import pprint as pp
from rich import print as rprint
from nornir.core.filter import F
from pprint import pprint
from datetime import datetime
import pathlib
from nornir_utils.plugins.tasks.files import write_file
#import getpass
import threading

# Declare empty lists for three main port statuses
port_list = ["Host,Interface,Description,IPaddr,Protocol-Status,Link-Status,MTU,"]

# Prepare Directory structure
output_dir = "PortSummary"
# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
date_dir = output_dir + "/" + dt_string
# Make sure all directories exist
pathlib.Path(output_dir).mkdir(exist_ok=True)
pathlib.Path(date_dir).mkdir(exist_ok=True)


# Specify Nornir config file
nr = InitNornir(config_file="config_vios.yaml")

# Uncomment below to enter password manualy
# username = input('Enter your username: ')
# password = getpass.getpass()

LOCK = threading.Lock()

with open(f"{date_dir}/interface-list.csv", "a") as f:
    f.write(f"Host,Interface,Speed,Duplex,Description,IPaddr,Protocol-Status,Link-Status,MTU\n")
# Task declaration
def show_interfaces(task):
    """
    Nornir Task for retreiving and processing interface status
    """
    intf_status = task.run(task=send_command, command="show interfaces")
    task.host["intlist"] = intf_status.scrapli_response.textfsm_parse_output() 
    interfaces = task.host["intlist"]
    
    for interface in interfaces:
        # try:
        LOCK.acquire()
        # except KeyError:
        #     pass
        port = interface["interface"]
        port_status = interface["link_status"]
        protocol_status = interface["protocol_status"] 
        description = interface["description"]
        mac_addr = interface["address"] 
        input_errors = interface["input_errors"] 
        input_packets = interface["input_packets"] 
        mtu = interface["mtu"] 
        output_packets = interface["output_packets"] 
        output_errors = interface["output_errors"] 
        vlan_id = interface["vlan_id"] 
        crc = interface["crc"]
        ip_address= interface["ip_address"]
        speed = interface["speed"]
        duplex = interface["duplex"]
        print(f"""
        HOST: {task.host}
        Interface {port} is {port_status} / {protocol_status},
        Description: {description}
        IP address: {ip_address}
        MAC: {mac_addr}
        MTU: {mtu}
        Input packets: {input_packets} , input errors: {input_errors}
        Output packets:{output_packets}, output errors: {output_errors}
        CRC errors: {crc }
        """)
        #port_list = ["Host,Interface,Description,IPaddr,Protocol-Status,Link-Status,MTU,"]
        port_list.append(f"['{task.host}','{port}','{speed}','{duplex}' ,'{description}','{ip_address}','{protocol_status}','{port_status}','{mtu}']")
        with open(f"{date_dir}/interface-list.csv", "a") as f:
            f.write(f"{task.host},{port},{speed},{duplex},{description},{ip_address},{protocol_status},{port_status},{mtu}\n")
        LOCK.release()
        #no_description.append(f"['{task.host}','{port}']")
# Filter target device group
#switch_target = nr.filter(F(groups__contains="distribution") | F(groups__contains="access") )
# Run Nornir task via function show_interfaces
#results = switch_target.run(task=show_interfaces)
results = nr.run(task=show_interfaces)
print(f"\nPlease check the output in {date_dir}/interface-list.csv File\n")
#print_result(results)
#pprint(port_list)

#ipdb.set_trace()