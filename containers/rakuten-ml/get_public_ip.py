import requests

def get_public_ip():
    """Get public IP from cloud metadata services"""
    try:
        # Try AWS
        response = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4', timeout=2)
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    
    try:
        # Try Azure
        response = requests.get(
            'http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2017-08-01',
            headers={'Metadata': 'true'},
            timeout=2
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    try:
        # Try GCP
        response = requests.get(
            'http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip',
            headers={'Metadata-Flavor': 'Google'},
            timeout=2
        )
        if response.status_code == 200:
            return response.text.strip()
    except:
        pass
    
    return "localhost"