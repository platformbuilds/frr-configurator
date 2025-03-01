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
    
    svc_listing = v1.list_service_for_all_namespaces(watch=False)
    
    for svc in svc_listing.items:
        svc_name = svc.metadata.name
        svc_namespace = svc.metadata.namespace
        svc_cluster_ips = svc.spec.cluster_i_ps
        svc_data = {
            "service_name": svc_name,
            "service_namespace": svc_namespace,
            "service_cluster_ips": svc_cluster_ips
        }
        print(svc_data)

else:
    logging.error("Kubeconfig not found !")
    quit()
