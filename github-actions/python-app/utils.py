import requests

def get_status_code(url: str) -> int:
    response = requests.get(url, timeout=5)
    return response.status_code
