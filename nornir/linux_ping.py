#!/usr/bin/env python3

"""
Crated by: swietlas
This is script test target devices directly from management PC
"""
import os
import subprocess
#from subprocess import Popen, DEVNULL
from rich import print as rprint

reachable = []
unreachable = []

# Clear output
os.system("clear")
os.system("rm reachable.txt ")
os.system("rm unreachable.txt ")

with open("target_list.txt", "r") as f:
    lines = f.readlines()
    # print("\nTarget hosts:")
    # print(lines)
    # print("*"*30)

for line in lines:
    ipaddr = str(line.rstrip())
    response = subprocess.Popen(["ping", "-c", "3", "-i", "0,2", "-w", "1", ipaddr],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)
    stdout, stderr = response.communicate()

    if response.returncode == 0:
        rprint(f"Target {ipaddr} is [green]reachable[/green]\n")
        reachable.append(line)
        with open("reachable.txt","a") as r_file:
            r_file.write(line)
    else:
        rprint(f"Target {ipaddr} is [red]unreachable[/red]\n")
        unreachable.append(line)
        with open("unreachable.txt","a") as unr_file:
            unr_file.write(line)