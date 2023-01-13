from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config_vios.yaml")

def another_show_command_test(task):
    task.run(task=netmiko_send_command, command_string="show interface GigabitEthernet0/0")

results = nr.run(task=another_show_command_test)
print_result(results)
#print_structured_result(result, parser="genie")