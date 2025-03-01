import netifaces

loopback_int_data = netifaces.ifaddresses("lo")

for int_index in loopback_int_data:
    for addresses in loopback_int_data[int_index]:
            for address_detail in addresses:
                    if address_detail["netmask"] == "255.255.255.255":
                            print(address_detail)