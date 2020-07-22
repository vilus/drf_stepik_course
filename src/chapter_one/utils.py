from typing import Any, Dict, List, Union

import requests
from django.core.cache import cache

RequestException = requests.exceptions.RequestException
HTTPError = requests.exceptions.HTTPError
Timeout = requests.exceptions.Timeout


def fetch_json(url: str, timeout: int) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    TODO
    """
    cached = cache.get(url)
    if cached:
        return cached

    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()

    res = resp.json()
    cache.set(url, res)
    return res
