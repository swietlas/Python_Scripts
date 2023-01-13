from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config_vios.yaml")

def pull_facts(task):
    task.run(task=napalm_get, getters=["get_facts"])

results = nr.run(task=pull_facts)
print_result(results)
