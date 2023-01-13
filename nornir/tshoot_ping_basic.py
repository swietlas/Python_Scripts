#!/usr/bin/env python3
"""
Created by: Swietalas

Script for simple connectivity test

"""

from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from rich import print as rprint

nr =InitNornir(config_file="config_vios.yaml")
unreachable = []

with open ("target_list.txt", "r") as f:
    lines = f.read().splitlines()

def ping_basic(task):
    for target in lines:
        result = task.run(task=send_command,command=f"ping vrf MGMT  {target}")
        response = result.result
        if not "!!!" in response:
            unreachable.append(f" {task.host} cannot ping {target}")

nr.run(task=ping_basic)
if unreachable:
    sorted_output = sorted(unreachable)
    print(sorted_output)
else:
    print("All pings were successfull")