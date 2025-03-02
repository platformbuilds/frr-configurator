import json
from config.kube.liveapps import get_kube_svc, get_my_ingress_pod_ip, get_kube_app_with_ingress_all

'''
check if node is ingress
list all the configured ingress apps
check if app on ingress is configurable
    yes: bring up the ClusterIP on FRR up
    no: bring down the ClusterIP on FRR down
loop every second !
'''



# fetch the running services and ingress pod IPs 
services = get_kube_svc()
node_ingress_details = get_my_ingress_pod_ip()
app_ingresses = get_kube_app_with_ingress_all()

print(json.dumps(services))
print(json.dumps(node_ingress_details))
print(json.dumps(app_ingresses))
