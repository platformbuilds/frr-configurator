import os
import sys
import subprocess
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../../../../')


def update_loopback_subprocess(ip, as_no):
    commands = f"""
    configure terminal
    interface lo
    ip address {ip}/32
    exit
    router bgp {as_no}
    address-family ipv4 unicast
    network {ip}/32
    end
    write memory
    end
    """

    try:
        process = subprocess.run(["vtysh"],input=commands, text=True, capture_output=True)

        if process.returncode == 0:
            print("FRR config updated successfully")
        else:
            print("error updating FRR conf:", process.stderr)
    except Exception as e:
        print("Exception occured", str(e))

def update_loopback_os(ip, as_no):
    commands = (
        f'vtysh -c "configure terminal" '
        f'-c "interface lo" '
        f'-c "ip address {ip}/32" '
        f'-c "exit" '
        f'-c "router bgp {as_no}" '
        f'-c "address-family ipv4 unicast" '
        f'-c "network {ip}/32" '
        f'-c "end" '
        f'-c "write memory" '
        f'-c "end" '
    )
    os.system(commands)