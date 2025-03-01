import json
from config.kubernetes import get_svc_ips

print(json.dumps(get_svc_ips))