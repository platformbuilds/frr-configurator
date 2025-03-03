import os
import logging
from kubernetes import client, config
from ..node.get_node_data import node_ips

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
            svc_cluster_ip = svc.spec.cluster_ip
            svc_data = {
                "service_name": str(svc_name),
                "service_namespace": str(svc_namespace),
                "service_cluster_ips": svc_cluster_ip
            }
            svc_list.append(svc_data)
    except Exception as e:
        logging.exception(e)
    return svc_list

def get_kube_app_with_ingress_all():
    logging.info("Listing all the ingress configs")
    app_ingresses = []
    try:
        networkingv1 = client.NetworkingV1Api()
        ingresses_dump = networkingv1.list_ingress_for_all_namespaces_with_http_info()[0].items
        for ingress_app in ingresses_dump:
            app_ingress_name = ingress_app.metadata.name
            app_ingress_namespace = ingress_app.metadata.namespace
            app_ingress_http_routes = []
            for rule in ingress_app.spec.rules:
                http_host = rule.host
                http_paths = []
                for path in rule.http.paths:
                    http_paths.append({"port":path.backend.service.port.number,"url":path.path,"url_prefix":path.path_type})
                app_ingress_http_routes.append({"http_host": http_host, "http_paths": http_paths})
            app_ingress = {
                "name": app_ingress_name,
                "namespace": app_ingress_namespace,
                "http_routes": app_ingress_http_routes
            }
            app_ingresses.append(app_ingress)

    except Exception as e:
        logging.exception(e)

    return app_ingresses


def get_kube_ingress_pods(ingress_namespace):
    logging.info("Listing ingress pods for {} namespace".format(ingress_namespace))
    ingress_pod_ips = []
    try:
        node_ip = node_ips()
        coreapiv1 = client.CoreV1Api()
        ingress_pods = coreapiv1.list_namespaced_pod(namespace=ingress_namespace).items
        for ingress_pod in ingress_pods:
            if ingress_pod.status.host_ip in node_ip:
                ingress_pod_ips.append(ingress_pod.status.pod_ip)
    except Exception as e:
        logging.exception(e)
    return ingress_pod_ips


def get_my_ingress_pod_ip():
    node_ingress_pod = []
    networkingv1 = client.NetworkingV1Api()
    try:
        logging.info("Listing ingress pods")
        ingress_classes = networkingv1.list_ingress_class().items
        for ingress_class in ingress_classes:
            ingress_namespace = ingress_class.metadata.annotations["meta.helm.sh/release-namespace"]
            ingress_pods = get_kube_ingress_pods(ingress_namespace)

            svc_list = get_kube_svc()
            ingress_svc = []
            for svc in svc_list:
                if ingress_class.metadata.annotations["meta.helm.sh/release-name"] in svc["service_name"]:
                    ingress_svc.append(svc["service_cluster_ips"])

            ingress = {
                "ingress_release_name": ingress_class.metadata.annotations["meta.helm.sh/release-name"],
                "ingress_release_namespace": ingress_class.metadata.annotations["meta.helm.sh/release-namespace"],
                "ingress_name": ingress_class.metadata.name,
                "ingress_pods": ingress_pods,
                "ingress_svc": ingress_svc
            }
            node_ingress_pod.append(ingress)
    except Exception as e:
        logging.exception(e)
    return node_ingress_pod

def get_kube_proxy_info():
    coreapiv1 = client.CoreV1Api()
    kube_proxy_pods = []
    try:
        node_ip = node_ips()
        kube_system_pods = coreapiv1.list_namespaced_pod(namespace="kube-system").items
        for pod in kube_system_pods:
            if "kube-proxy" in pod.metadata.name:
                if pod.status.host_ip in node_ip:
                    kube_proxy_pods.append({
                        "kube_proxy_name": pod.metadata.name,
                        "kube_proxy_namespace": pod.metadata.namespace,
                        "kube_proxy_node_ip": pod.status.host_ip,
                        "kube_proxy_pod_ip": pod.status.pod_ip
                        })
    except Exception as e:
        logging.exception(e)
    return kube_proxy_pods
    


def check_ingress_pod_health(ingress_pod_ip, ingress_host, ingress_ports_list):
    healthy = False
    '''
    get the node_ingress_pod
    check the app is giving a successful response --> RV Start here.
    '''
    return healthy
