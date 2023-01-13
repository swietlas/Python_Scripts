#!/usr/bin/env python3
"""
Crated by: swietlas

This is script retrieves and processes interface information from Cisco switches ans gather vlan and Voice vlan datea

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
output_dir = "VoiceVLAN"
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

with open(f"{date_dir}/interfaces_with_voice_vlan.csv", "a") as f:
    f.write(f"Host,Interface,Vlan,VoiceVLAN\n")
with open(f"{date_dir}/interfaces_with_no_voice_vlan.csv", "a") as f:    
    f.write(f"Host,Interface,Vlan\n")
with open(f"{date_dir}/trunk_interfaces_.csv", "a") as f:    
    f.write(f"Host,Interface,NativeVLAN,AllowedVLAns\n")
# Task declaration
def show_switchport(task):
    """
    Nornir Task for retreiving and processing interface status
    """
    intf_status = task.run(task=send_command, command="show interfaces switchport")
    task.host["intflist"] = intf_status.scrapli_response.textfsm_parse_output() 
    interfaces = task.host["intflist"]
    
    for interface in interfaces:

        LOCK.acquire()

        port = interface["interface"]
        mode = interface["mode"] # 'mode': 'trunk (member of bundle Po1)','mode': 'static access','mode': 'trunk',  'mode': 'down',
        admin_mode = interface["admin_mode"] # 'admin_mode': 'trunk',  'admin_mode': 'dynamic auto',  'admin_mode': 'static access',
        native_vlan = interface["native_vlan"]
        voice_vlan = interface["voice_vlan"]
        access_vlan = interface["access_vlan"]
        trunking_vlans = interface["trunking_vlans"]

        if mode == 'static access':
            print(f"""
                HOST: {task.host}
                Interface {port} is configured as Access Port
                VLAN: {access_vlan}
                Voice VLAN: {voice_vlan}
                """)

            if voice_vlan != 'none':
                print(voice_vlan)   
                with open(f"{date_dir}/interfaces_with_voice_vlan.csv", "a") as f:
                    f.write(f"{task.host},{port},{access_vlan},{voice_vlan}\n")
            else:
                print(voice_vlan)   
                with open(f"{date_dir}/interfaces_with_no_voice_vlan.csv", "a") as f:
                    f.write(f"{task.host},{port},{access_vlan}\n")

        if mode == 'trunk':
            print(f"""
                HOST: {task.host}
                Interface {port} is configured as TRUNK PORT
                Native VLAN: {native_vlan}
                Allowed VLANS:{trunking_vlans}
            """)

            with open(f"{date_dir}/trunk_interfaces_.csv", "a") as f:    
                f.write(f"{task.host},{port},{native_vlan},{trunking_vlans}\n")

        if "trunk (member of bundle" in mode:
            print(f"""
                HOST: {task.host}
                Interface {port} is configured as Etherchanel and Trunk
                Native VLAN: {native_vlan}
                Allowed VLANS:{trunking_vlans} 
            """)  

            with open(f"{date_dir}/trunk_interfaces_.csv", "a") as f:    
                f.write(f"{task.host},{port},{native_vlan},{trunking_vlans}\n")



        LOCK.release()

# Filter target device group
#switch_target = nr.filter(F(groups__contains="distribution") | F(groups__contains="access") )
# Run Nornir task via function show_interfaces
#results = switch_target.run(task=show_interfaces)
results = nr.run(task=show_switchport)
rprint(f"\nPlease check the output files in [green]{date_dir}[/green] directory\n")

#ipdb.set_trace()