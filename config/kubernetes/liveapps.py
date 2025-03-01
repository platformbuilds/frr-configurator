import os
import logging
from kubernetes import client, config

logging.basicConfig(
    format='{\"timestamp\":\"%(asctime)s\",\"log_level\":\"%(levelname)s\",\"message\":\"%(message)s\",\"app\":\"%(name)s\"}',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S.000Z',
    )

if os.path.isfile("/root/.kube/config"):
    config.load_kube_config()
    logging.info("successfully loaded kubeconfig")
else:
    logging.error("kubeconfig not found. ensure node is a valid kube node")

def get_kube_svc():
    svc_list = []
    try:
        logging.info("Listing running services")
        coreapiv1 = client.CoreV1Api()
        svc_listing = coreapiv1.list_service_for_all_namespaces(watch=False)
        for svc in svc_listing.items:
            svc_name = svc.metadata.name
            svc_namespace = svc.metadata.namespace
            svc_cluster_ips = svc.spec.cluster_i_ps
            svc_data = {
                "service_name": str(svc_name),
                "service_namespace": str(svc_namespace),
                "service_cluster_ips": str(svc_cluster_ips)
            }
            svc_list.append(svc_data)
    except Exception as e:
        logging.exception(e)
    return svc_list

# --> RV resume here...
def get_my_ingress_pod_ip():
    node_ingress_pod = []
    networkingv1 = client.NetworkingV1Api()
    try:
        logging.info("Listing ingress pods")
        ingress_classes = networkingv1.list_ingress_class().items
        for ingress_class in ingress_classes:
            ingress = {
                "ingress_release_name": ingress_class.metadata.annotations["meta.helm.sh/release-name"],
                "ingress_release_namespace": i.metadata.annotations["meta.helm.sh/release-namespace"],
                "ingress_name": i.metadata.name
            }
            node_ingress_pod.append(ingress)
    except Exception as e:
        logging.exception(e)
    return node_ingress_pod