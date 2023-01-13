#!/usr/bin/env python3
"""
Crated by: swietlas

This is script retrieves and processes interface status from Cisco network devicess

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
from nornir_scrapli.functions import print_structured_result
from nornir_utils.plugins.functions import print_result
import pprint as pp
from rich import print as rprint
from datetime import datetime
import pathlib
import ipdb
import genie

# Prepare Directory structure
output_dir = "DevicesInfo"
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

# Prompt for credential
# username = input('Enter your username: ')
# password = getpass.getpass()

# Set Header line for CSV file
with open(f"{date_dir}/inventory.csv", "a") as f:
    f.write(f"Host,Chassis,Chassis_SN,Platform,DeviceType,SystemImage,Version,Version_Short,Release,Uptime,DRAMsize,FlashSize\n")
rprint("[yellow]Connecting to all devices in scope and collecting inventory information - please wait[/yellow]\n")

# Define Norninr taks
def get_facts(task):
    collected = task.run(task=send_command, command="show version")
    task.host["facts"] = collected.scrapli_response.genie_parse_output()
    device = task.host["facts"]["version"]
    chassis = device["chassis"]
    chassis_sn = device["chassis_sn"]
    flash = device["mem_size"]["non-volatile configuration"]
    DRAM = device["main_mem"]
    device_type = device["rtr_type"]
    system_image = device["system_image"]
    platform = device["platform"]
    uptime = device["uptime"]
    uptime = uptime.replace(","," ") # this removes comma from uptime string 'uptime': '2 hours, 4 minutes'
    version = device["version"]
    version_sort = device["version_short"]
    release = device["label"]
    # Save to file
    with open(f"{date_dir}/inventory.csv", "a") as f:
        f.write(f"{task.host},{chassis},{chassis_sn},{platform},{device_type},{system_image},{version},{version_sort},{release},{uptime},{DRAM},{flash}\n")

# Run Nornir task
result = nr.run(task=get_facts)
# Print location of target file
rprint(f"\nPlease find target inventory file here:  [green]'{date_dir}/inventory.csv'[/green] \n")
#print_structured_result(result)


ipdb.set_trace()
