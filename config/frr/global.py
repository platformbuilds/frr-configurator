'''
This script generates the global config section in FRR Routing Software.
'''
import os
import json
import socket


config_tpl = {
    "global": []
}

# Defining all config parameters
hostname = "hostname {}".format(socket.gethostname())
frr_bgpd_version = os.popen("/usr/lib/frr/bgpd -v | grep version").read().replace("bgpd","frr").replace("\n","")
log_mode = "syslog"
log_level = "informational"
log_config = "log {} {}".format(log_mode, log_level)
ipv4_forwarding = True
ipv6_forwarding = False


global_config = [
    frr_bgpd_version,
    "frr defaults traditional",
    hostname,
    log_config,
    "ipv4 forwarding",
    "no ipv6 forwarding",
    "service integrated-vtysh-config",
    "!"
]

