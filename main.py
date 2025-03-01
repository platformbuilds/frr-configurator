import json
from config.kubernetes.get_svc_ips import get_kube_svc


print(json.dumps(get_kube_svc()))