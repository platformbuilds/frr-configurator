import json
from config.kubernetes.get_svc_ips import get_kube_svc

services = get_kube_svc()
print(type(services))
print(services)