import json, csv, os, sys, requests
sys.path.append("../../../")
from common.readCsv import get_ip_for_hostname, read_json_for_hostname

class BgpGlobal:
    def __init__(self, username, password):
        # Initializing credentials
        self.username = username
        self.password = password

    def get_config(self, host):
        # GET request to fetch the configuration
        try:
            ip = get_ip_for_hostname(host)
            url = f'https://{ip}/restconf/data/sonic-bgp-global:sonic-bgp-global'
            response = requests.get(url, auth=requests.auth.HTTPBasicAuth(self.username, self.password), verify=False)
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
            
            url = f'https://{ip}/restconf/data/sonic-bgp-global:sonic-bgp-global'
            json_data = read_json_for_hostname(host,'bgpGlobal') # host and path
            
            if json_data is None:
                print(f"Error: No JSON configuration found for {host}")
                return
            
            headers = {'Content-Type': 'application/yang-data+json'}
            
            print(f"Sending PUT request to {url} with data: {json_data}")  # Debugging
            
            response = requests.post(url, auth=requests.auth.HTTPBasicAuth(self.username, self.password),
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
    bgp_global = BgpGlobal(username='admin', password='npci@123')
    
    # Call GET method to fetch the configuration
    bgp_global.get_config('edge_leaf1')
    bgp_global.post_config('edge_leaf1')
    # bgp_config.get_config('edge_leaf1')


if __name__ == "__main__":
    main()