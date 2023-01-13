from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_ping
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config_vios.yaml")

def ping_test(task):
    task.run(task=napalm_ping, dest="10.10.7.254", vrf="MGMT")

results = nr.run(task=ping_test)
print_result(results)
