def read_url(url: str, **kwargs) -> str:
    import requests
    return requests.get(url, **kwargs, timeout=5).text
