#!/usr/bin/env python
"""
Author: Marcin Switilnik

This is script retrieves and processes CDP data from network devices

Don't forget to install scrapli, norninr_scrapli, nornir utils, textfsm and genie
pip install nornir scrapli

pip install genie pyats
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



nr = InitNornir(config_file="config_vios.yaml")

def show_neighbors(task):
    cdp_result = task.run(task=send_command, command="show cdp neighbors")
    # In order to use print_structured_result please comment following line
    task.host["cdpinfo"] = cdp_result.scrapli_response.genie_parse_output()
        # At this point we can simply work with that `scrapli_response` like we would a "normal" scrapli
    # response object:
    #textfsm_results = host_result.scrapli_response.textfsm_parse_output()
    #genie_results = host_result.scrapli_response.genie_parse_output()
    index = task.host["cdpinfo"]["cdp"]["index"]


    for num in index:
        local_intf = index[num]["local_interface"]
        if local_intf == intf:
            dev_id = index[num]["device_id"]
            port_id = index[num]["port_id"]

results = nr.run(task=show_neighbors)
# In order to use print_structured_result with Genie or TextFsm please comment following line
print_result(results)
# print_structured_result(results, parser="genie")
# print_structured_result(results, parser="textfsm")

# for Debuging purpose set trace
# ipdb.set_trace()