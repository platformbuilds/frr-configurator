import os
import logging
from kubernetes import client, config

logging.basicConfig(
    format='{\"timestamp\":\"%(asctime)s\",\"log_level\":\"%(levelname)s\",\"message\":\"%(message)s\",\"app\":\"%(name)s\"}',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S.000Z',
    )

def get_kube_svc():
    svc_list = []
    if os.path.isfile("/root/.kube/config"):
        config.load_kube_config()
        v1 = client.CoreV1Api()
        logging.info("Listing running services")
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
            svc_list.append(svc_data)

    else:
        logging.error("Kubeconfig not found !")

    return svc_list
