import requests
from requests.auth import HTTPBasicAuth
import json, csv, os
from readCsv import get_ip_for_hostname, read_json_for_hostname

class BgpPeergroup:
    def __init__(self, username, password):
        # Initializing credentials
        self.username = username
        self.password = password

    def get_config(self, host):
        # GET request to fetch the configuration
        try:
            ip = get_ip_for_hostname(host)
            url = f'https://{ip}/restconf/data/sonic-bgp-peergroup:sonic-bgp-peergroup'
            response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), verify=False)
            # Check for successful response
            if response.status_code == 200:
                print("GET Request Successful:")
                print(response.text)
            else:
                print(f"Failed GET request with status code {response.status_code}")
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def post_config(self, host):
        # PUT request to update the configuration
        try:
            ip = get_ip_for_hostname(host)
            if ip is None:
                print(f"Error: No IP found for hostname {host}")
                return
            
            url = f'https://{ip}/restconf/data/sonic-bgp-peergroup:sonic-bgp-peergroup'
            json_data = read_json_for_hostname(host,'bgpPeer')
            
            if json_data is None:
                print(f"Error: No JSON configuration found for {host}")
                return
            
            headers = {'Content-Type': 'application/yang-data+json'}
            
            print(f"Sending PUT request to {url} with data: {json_data}")  # Debugging
            
            response = requests.post(url, auth=HTTPBasicAuth(self.username, self.password),
                                    headers=headers, data=json.dumps(json_data), verify=False)
            
            if response.status_code == 200:
                print("PUT Request Successful:")
                print(response.text)
            else:
                print(f"Failed POST request with status code {response.status_code}")
                print(f"Response body: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

def main():
    print("In main")

    # Create an instance of the BgpPeergroup class
    bgp_config = BgpPeergroup(username='admin', password='npci@123')
    
    # Call GET method to fetch the configuration
    bgp_config.get_config('edge_leaf1')
    #bgp_config.post_config('edge_leaf1')
    # bgp_config.get_config('edge_leaf1')


if __name__ == "__main__":
    main()