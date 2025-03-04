import os,json,csv

def get_ip_for_hostname(hostname):
    """Reads the CSV file and returns the IP address for a given hostname."""
    try:
        file_path='./static/hosts.csv'
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                if row[0] == hostname:  # Check if the current row matches the hostname
                    return row[1]  # Return the IP address for the matched hostname
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
    return None  # Return None if the hostname was not found

def read_json_for_hostname(hostname, path):
    """Reads the JSON configuration for a given hostname from the static folder."""
    json_file_path = f"./static/{path}/{hostname}.json"
    
    if not os.path.exists(json_file_path):
        print(f"Error: The JSON file for {hostname} does not exist in the 'static/' folder.")
        return None
    
    with open(json_file_path, 'r') as file:
        return json.load(file)