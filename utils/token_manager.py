import requests
from config.api_config import API_BASE_URL, TOKEN_URL, CLIENT_AUTH

_token = None

def get_access_token():
    global _token

    if _token:
        return _token

    url = API_BASE_URL + TOKEN_URL

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": CLIENT_AUTH
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        _token = response.json().get("access_token")
        return _token

    return None