#!/usr/bin/env python3
"""
Crated by: swietlas

This is script retrieves interface information using "show interface description" command
and processes gathered data in order to select interfaces without description.
Then it adds description "Disabled by Admin" and shutdown all portrs in scope.

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

import csv
from nornir import InitNornir
from nornir_scrapli.tasks import send_command,send_configs
from nornir_scrapli.functions import print_structured_result
import ipdb
from rich import print as rprint
from nornir.core.filter import F
from pprint import pprint
from datetime import datetime
import pathlib
#from nornir_utils.plugins.tasks.files import write_file
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

# Uncomment below to enter password manualy
# username = input('Enter your username: ')
# password = getpass.getpass()

no_description = []
LOCK = threading.Lock()
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
        intf = port
        if ("Po" in port or "." in port or "Vl" in port or "Lo" in port ):
            rprint(f"[yellow]{task.host}: Ignoring logical interface {port} [/yellow]")
        elif description == "":
            if protocol == "up":
                rprint(f"[red]{task.host}:  {port} has no Description and is in {protocol}/{status} [/red]")
            else:
                rprint(f"[medium_purple2]{task.host}:  {port} has no Description and is in {protocol}/{status} [/medium_purple2]")
            # For debugging purpose script saves ports which should be disabled in CSV format    
            with open( f"{date_dir}/ports_to_shut.csv", "a") as f:
                f.write(f"{task.host},{port}\n")
                no_description.append(f"['{task.host}','{port}']")
                command_list = [ str("interface" +" " +  port),"shutdown","description Disabled by Admin"]
                disable_unused(task, command_list )
                # disable_unused(task, port,command_list )
        else:    
            rprint(f"[green]{task.host}:  {port} has following Description: {description} And is in {protocol}/{status}[/green] ")
        LOCK.release()

def disable_unused(task,input_list):
    task.run(task=send_configs, name="disable interfaces", configs=input_list,)


# In order to filter target device group please uncomment and adjust accordingly
# switch_target = nr.filter(F(groups__contains="distribution") | F(groups__contains="access") )
# Run Nornir task via function show_interfaces
# results = switch_target.run(task=show_interfaces)
print("#"*75)
print("Retrieving and processing interface information")
print("#"*75)
results = nr.run(task=show_interfaces)
print("#"*75)
print("List of ports to be disabled")
print("#"*75)
pprint(no_description)

#ipdb.set_trace()