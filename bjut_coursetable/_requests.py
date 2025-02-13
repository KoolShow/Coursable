import requests

def read_url(url: str, **kwargs) -> str:
    return requests.get(url, **kwargs).text