import requests

class APIInterface:
    def __init__(self, base_url):
        self.base_url = base_url

    def _send_get_request(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        return response.json()

    def _send_post_request(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, json=data)
        return response.json()

    def _send_put_request(self, endpoint, data=""):
        url = f"{self.base_url}/{endpoint}"
        response = requests.put(url, json=data)
        return response.json()

    def _send_delete_request(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        response = requests.delete(url)
        return response.json()
