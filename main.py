import json
from config.kube.liveapps import get_kube_svc, get_my_ingress_pod_ip


# fetch the running services and ingress pod IPs 
services = get_kube_svc()
ingress = get_my_ingress_pod_ip()

print(services)
print(ingress)

'''
# Check if the current svc can be handled by the node - self check
Check the status of the ingress pod on the current node
if present, check its health for the service being added
and if all good, then create a list of service ips to be added to FRR loopback interfaces
'''

# build the vtysh config

