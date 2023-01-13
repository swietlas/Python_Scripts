#!/usr/bin/env python3
'''
Created by swietlas

This scripts creates backup of running config for IOS and IOSXE devices

'''

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
import pathlib
from datetime import datetime


nr = InitNornir(config_file="config_vios.yaml")

def prepare_dirs():
    # Prepare Directory structure
    output_dir = "Backups"
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
    date_dir = output_dir + "/" + dt_string
    # Make sure all directories exist
    pathlib.Path(output_dir).mkdir(exist_ok=True)
    pathlib.Path(date_dir).mkdir(exist_ok=True)
    return date_dir

def backup_configs(task,config_dir):
    cfg_result = task.run(task=napalm_get, getters=["config"])
    startup_cfg = cfg_result.result["config"]["running"]
    task.run(task=write_file, content=startup_cfg, filename=f"{date_result}/{task.host}.cfg")

print("\n[Step 1] Maing sure directory structure exists\n")
date_result = prepare_dirs()
# calling napalm task
print("[Step 2] Running Norninr tasks\n")
results = nr.run(task=backup_configs, config_dir=date_result)
# optionally you can print output to screen
#print_result(results)
print(f"[Completed] You can find backup files in {date_result}")