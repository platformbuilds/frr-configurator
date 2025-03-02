import json
from config.kube.liveapps import get_kube_svc, get_my_ingress_pod_ip, get_kube_app_with_ingress_all


# fetch the running services and ingress pod IPs 
services = get_kube_svc()
node_ingress_details = get_my_ingress_pod_ip()
app_ingresses = get_kube_app_with_ingress_all()

print(services)
print(node_ingress_details)
print(app_ingresses)

'''
# Check if the current svc can be handled by the node - self check
Check the status of the ingress pod on the current node
if present, check its health for the service being added
and if all good, then create a list of service ips to be added to FRR loopback interfaces
'''

# build the vtysh config

