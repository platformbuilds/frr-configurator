import json
from config.kubernetes.liveapps import get_kube_svc


# fetch the running services and ingress pod IPs 
services = get_kube_svc()
ingress = get_my_ingress_pod_ip()

# Check if the current svc can be handled by the node - self check
'''
Check the 
'''

# build the vtysh config

