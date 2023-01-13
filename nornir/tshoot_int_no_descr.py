#!/usr/bin/env python3
"""
Crated by: swietlas

This is script retrieves and processes interface status from Cisco network devices

Don't forget to install scrapli, norninr_scrapli, nornir utils, textfsm and genie

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

# Prepare Directory structure
output_dir = "IntNoDescr"
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
LOCK = threading.Lock()
# Uncomment below to enter password manualy
# username = input('Enter your username: ')
# password = getpass.getpass()

# Task declaration
def show_interfaces(task):
    """
    Nornir Task for retreiving and processing interface status
    """
    intf_status = task.run(task=send_command, command="show interfaces description")
    task.host["intlist"] = intf_status.scrapli_response.textfsm_parse_output() 
    interfaces = task.host["intlist"]
    
    for interface in interfaces:
        LOCK.acquire()
        port = interface["port"]
        protocol = interface["protocol"]
        status = interface["status"]
        description = interface["descrip"]
        #rprint(f"{task.host}  {port} with label {description} is in {protocol}/{status} ")
        if ("Po" in port or "." in port or "Vl" in port or "Lo" in port ):
            rprint(f"[yellow]{task.host}: Ignoring logical interface {port} [/yellow]")

        elif description == "":
            if protocol == "up":
                rprint(f"[red]{task.host}:  {port} has no Description and is in {protocol}/{status} [/red]")
            else:
                rprint(f"[medium_purple2]{task.host}:  {port} has no Description and is in {protocol}/{status} [/medium_purple2]")

        else:    
            rprint(f"[green]{task.host}  {port} has label {description} is in {protocol}/{status}[/green] ")
        LOCK.release()
# Filter target device group
#switch_target = nr.filter(F(groups__contains="distribution") | F(groups__contains="access") )
# Run Nornir task via function show_interfaces
# results = switch_target.run(task=show_interfaces)
results = nr.run(task=show_interfaces)
#print_result(results)
#ipdb.set_trace()