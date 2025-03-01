import netifaces

loopback_int_data = netifaces.ifaddresses("lo")

for int_index in loopback_int_data:
    for addresses in loopback_int_data[int_index]:
            for address_details in addresses:
                    for address in address_details:
                        print(address)