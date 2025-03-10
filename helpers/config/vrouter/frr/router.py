import os
import sys
import subprocess
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format the log messages
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to standard output
    ]
)

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../../../../')


def add_loopback_subprocess(ip):
    commands = f"""
    configure terminal
    interface lo
    ip address {ip}/32
    end
    write memory
    end
    """

    try:
        process = subprocess.run(["vtysh"], input=commands, text=True, capture_output=True)

        if process.returncode == 0:
            logging.info("FRR config updated successfully")
        else:
            logging.error(f"Error updating FRR config: {process.stderr}")
    except Exception as e:
        logging.exception("Exception occurred while updating FRR config")


def add_loopback_os(ip):
    commands = (
        f'vtysh -c "configure terminal" '
        f'-c "interface lo" '
        f'-c "ip address {ip}/32" '
        f'-c "end" '
        f'-c "write memory" '
        f'-c "end" '
    )
    try:
        os.system(commands)
        logging.info(f"Loopback {ip} added to OS successfully.")
    except Exception as e:
        logging.exception(f"Exception occurred while adding loopback {ip} to OS")


def remove_loopback_os(ip):
    commands = (
        f'vtysh -c "configure terminal" '
        f'-c "interface lo" '
        f'-c "no ip address {ip}/32" '
        f'-c "end" '
        f'-c "write memory" '
        f'-c "end" '
    )
    try:
        os.system(commands)
        logging.info(f"Loopback {ip} removed from OS successfully.")
    except Exception as e:
        logging.exception(f"Exception occurred while removing loopback {ip} from OS")


def main():
    # Example usage - replace with actual IP and AS number
    ip = "10.40.21.10"

    # Add loopback via subprocess
    add_loopback_subprocess(ip)

    # Add loopback via OS command
    #add_loopback_os(ip)

    # Remove loopback via OS command (if needed)
    #remove_loopback_os(ip)


if __name__ == "__main__":
    main()
