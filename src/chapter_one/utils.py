from typing import Any, Dict, List, Union

import requests

RequestException = requests.exceptions.RequestException
HTTPError = requests.exceptions.HTTPError
Timeout = requests.exceptions.Timeout


def fetch_json(url: str, timeout: int) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()
