import os
import json
import logging
from kubernetes import client, config

logging.basicConfig(
    format='{\"timestamp\":\"%(asctime)s\",\"log_level\":\"%(levelname)s\",\"message\":\"%(message)s\",\"app\":\"%(name)s\"}',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S.000Z',
    )

if os.path.isfile("/root/.kube/config"):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_service_for_all_namespaces(watch=False)
    for svc in ret.items:
        print(json.dumps(svc))

else:
    logging.error("Kubeconfig not found !")
    quit()
