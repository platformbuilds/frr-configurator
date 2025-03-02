import json
from config.kube.liveapps import get_kube_svc, get_my_ingress_pod_ip, get_kube_app_with_ingress_all

'''
Check if node is eligible and healthy for
    kube-proxy
    ingress

list all the svc on the k8s cluster

categorise them to L4-Kube-Proxy and L7-IngressClass
    yes: bring up the ClusterIP on FRR up
    no: bring down the ClusterIP on FRR down

loop every second !

'''


# fetch the running services and ingress pod IPs 
services = get_kube_svc()
app_ingresses = get_kube_app_with_ingress_all()
node_ingress_details = get_my_ingress_pod_ip()

# Blindly advertise the ClusterIP of Ingress Service if node is eligible
svc_list = []
for svc in services:
    svc_list.append(svc["service_name"])

l7_ingress_services_to_expose = []
for app_ingress in app_ingresses:
    l7_ingress_services_to_expose.append(app_ingress["name"])

# Check the health of each service and then expose the ClusterIP if the node is able to handle the traffic
l4_kube_proxy_services_to_expose = []
for svc in services:
    if svc["service_name"] not in l7_ingress_services_to_expose:
        l4_kube_proxy_services_to_expose.append(svc)


print("{}\n".format(json.dumps(services)))
print("{}\n".format(json.dumps(app_ingresses)))
print("{}\n".format(json.dumps(node_ingress_details)))
print("{}\n".format(json.dumps(l7_ingress_services_to_expose)))
print("{}\n".format(json.dumps(l4_kube_proxy_services_to_expose)))
