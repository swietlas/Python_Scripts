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
import getpass


# Declare empty lists for three main port statuses
connected_ports = ["Host,Port,Description"]
notconnected_ports = ["Host,Port,Description"]
err_disabled_ports =["Host,Port,Description"]
disabled_ports = ["Host,Port,Description"]

# Prepare Directory structure
output_dir = "PortStatus"
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
username = input('Enter your username: ')
password = getpass.getpass()
# Task declaration
def show_interfaces(task):
    """
    Nornir Task for retreiving and processing interface status
    """
    intf_status = task.run(task=send_command, command="show interface status")
    task.host["list"] = intf_status.scrapli_response.textfsm_parse_output() 
    interfaces = task.host["list"]
    
    for interface in interfaces:
        port = interface["port"]
        port_status = interface["status"]
        description = interface["name"]
        if port_status == "connected":
            connected_ports.append(f"{task.host},{port},{description}")
        elif port_status == "notconnect":
            notconnected_ports.append(f"{task.host},{port},{description}")
        elif port_status == "err-disabled":
            err_disabled_ports.append(f"{task.host},{port},{description}")
        elif port_status == "disabled":
            disabled_ports.append(f"{task.host},{port},{description}")

def SaveAndPrint(status):
    """
    Function prints the result on screen and save output to respective file
    """
    # Preparing output based on interface status
    if status == "connected":
        print("\n"+"#"*75)
        rprint("[green]CONNECTED[/green]")
        port_list = connected_ports
    elif status == "notconnect":
        print("\n"+"#"*75)
        rprint("[yellow]DISCONNECTED[/yellow]")
        port_list = notconnected_ports
    elif status == "err-disabled":
        print("\n"+"#"*75)
        rprint("[red]ERROR DISABLED[/red]")
        port_list = err_disabled_ports
    elif status == "disabled":
        print("\n"+"#"*75)
        rprint("[medium_purple2]DISABLED[/medium_purple2]")
        port_list = disabled_ports  
    # Save content of given list to file
    with open( f"{date_dir}/{status}.txt", "w") as f:
        for line in port_list:
            print(line)
            f.write(line + "\n")


# Filter target device group
switch_target = nr.filter(F(groups__contains="distribution") | F(groups__contains="access") )
# Run Nornir task via function show_interfaces
results = switch_target.run(task=show_interfaces)

status_list = ["connected","notconnect","err-disabled","disabled"]
for s in status_list:
    SaveAndPrint(s)
print(f"\nPlease find output files in {date_dir} directory")    