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
#from nornir_scrapli.functions import print_structured_result
from nornir_utils.plugins.functions import print_result
import pprint as pp
from rich import print as rprint
#from datetime import datetime
#import pathlib
import ipdb
import genie
import threading
import getpass

# Prepare Directory structure if needed
#output_dir = "IOS_Dir"
# datetime object containing current date and time
#now = datetime.now()
# dd/mm/YY H:M:S
#dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
#date_dir = output_dir + "/" + dt_string
# Make sure all directories exist
#pathlib.Path(output_dir).mkdir(exist_ok=True)
#pathlib.Path(date_dir).mkdir(exist_ok=True)
LOCK= threading.Lock()
LOCK1= threading.Lock()
# Specify Nornir config file
nr = InitNornir(config_file="config_vios.yaml")

# Prompt for credential
# username = input('Enter your username: ')
# password = getpass.getpass()


# Define Norninr taks:

def get_facts(task):
    collected = task.run(task=send_command, command="show version")
    task.host["facts_ver"] = collected.scrapli_response.genie_parse_output()
    device = task.host["facts_ver"]["version"]
    chassis = device["chassis"]
    chassis_sn = device["chassis_sn"]
    flash = device["mem_size"]["non-volatile configuration"]
    DRAM = device["main_mem"]
    device_type = device["rtr_type"]
    system_image = device["system_image"]
    platform = device["platform"]
    uptime = device["uptime"]
    uptime = uptime.replace(","," ") # this removes comma from uptime string to not break CSV file. For instance: 'uptime': '2 hours, 4 minutes'
    version = device["version"]
    version_sort = device["version_short"]
    release = device["label"]
    LOCK1.acquire()
    task.host["sys_image"] = system_image
    LOCK1.release()

def get_flash_info(task):
    collected = task.run(task=send_command, command="dir")
    task.host["facts"] = collected.scrapli_response.genie_parse_output()
    flash = task.host["facts"]["dir"]["dir"]
    flash_total = task.host["facts"]["dir"][flash]["bytes_total"]
    flash_free = task.host["facts"]["dir"][flash]["bytes_free"]
    files = task.host["facts"]["dir"][flash]["files"]
    LOCK.acquire()

    systemimage = task.host["sys_image"]

    if str(task.host) == "HQ":
        systemimage_extr = systemimage.split(":")[1]
    else:
        systemimage_extr = systemimage.split(":/")[1]

    print(f"""
    
************************************************************

               [ {task.host} ]    
    Toatal Flash space: {flash_total}
    Free Flash space: {flash_free}
    FLASH part: System image is: {systemimage}
    And here are all files stored on {flash}
     
    """)   

    for file in files:
        #print(file)
        if file == systemimage_extr:
            rprint(f"[green]IOS file found:[/green] {file}")
        else:
            print(file)
   #print("*"*60)
    LOCK.release()

# Run this if called by script not just imported in other script
if __name__ == "__main__":
    # Run Nornir task
    result = nr.run(task=get_facts)
    result2 = nr.run(task=get_flash_info)
    #result = nr.run(task=get_flash_info)
    # Print location of target file
    #rprint(f"\nPlease find target inventory file here:  [green]'{date_dir}/inventory.csv'[/green] \n")
    #print_structured_result(result)


    #ipdb.set_trace()
