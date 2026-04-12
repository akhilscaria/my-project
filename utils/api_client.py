import requests
from config.api_config import API_BASE_URL
from utils.token_manager import get_access_token


class APIClient:

    def _headers(self):
        token = get_access_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

    def get(self, endpoint, extra_headers=None):
        headers = self._headers()

        if extra_headers:
            headers.update(extra_headers)

        return requests.get(API_BASE_URL + endpoint, headers=headers)

    def post(self, endpoint, data):
        return requests.post(API_BASE_URL + endpoint, json=data, headers=self._headers())

    def put(self, endpoint, data):
        return requests.put(API_BASE_URL + endpoint, json=data, headers=self._headers())

    def delete(self, endpoint, data):
        return requests.delete(API_BASE_URL + endpoint, json=data, headers=self._headers())