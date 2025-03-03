import os
import sys
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../../../')
import logging
import netifaces

logging.basicConfig(
    format='{\"timestamp\":\"%(asctime)s\",\"log_level\":\"%(levelname)s\",\"message\":\"%(message)s\",\"app\":\"%(name)s\"}',
    level=logging.INFO,
    datefmt='%Y-%m-%dT%H:%M:%S.000Z',
    )

def node_ips():
    node_ips = []
    loopback_int_data = netifaces.ifaddresses("lo")
    for int_index in loopback_int_data:
        for addresses in loopback_int_data[int_index]:
            try:
                if addresses["netmask"] == "255.255.255.255":
                    node_ips.append(addresses["addr"])
            except KeyError:
                logging.warn("{} looks like a bgp peer interface. skipping".format(addresses["addr"]))
                pass
    return node_ips
