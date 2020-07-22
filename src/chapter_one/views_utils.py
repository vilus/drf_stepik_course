from typing import Any, Callable, Dict, Optional, List, Union

from django.http import QueryDict
from rest_framework import exceptions
from rest_framework import status

from chapter_one import utils


class RequestTimeoutError(exceptions.APIException):
    status_code = status.HTTP_408_REQUEST_TIMEOUT
    default_detail = 'Request timeout.'
    default_code = 'request_timeout_error'


def fetch_json(url: str, timeout: int) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    TODO
    """
    try:
        return utils.fetch_json(url, timeout)
    except utils.HTTPError as e:
        raise exceptions.APIException(detail=e.response.reason, code=e.response.status_code)
    except utils.Timeout:
        raise RequestTimeoutError()
    except Exception:
        raise exceptions.APIException()


def get_min_from_query_dict_by_key(query_dict: QueryDict, key: str) -> int:
    """
    TODO
    """
    return min(int(i) for i in query_dict.getlist(key))


def get_query_params(query_params: QueryDict,
                     param_getter_map: Dict[str, Callable[[QueryDict], Any]]) -> Dict[str, Any]:
    """
    TODO:
    """
    unexpected_params = set(query_params.keys()) - set(param_getter_map.keys())
    if unexpected_params:
        raise exceptions.ValidationError(detail=f'unexpected params: {unexpected_params}')

    res = {}
    errs = []
    for param_key in param_getter_map.keys():
        if param_key not in query_params:
            continue
        try:
            res[param_key] = param_getter_map[param_key](query_params)
        except Exception:
            errs.append(param_key)

    if errs:
        raise exceptions.ValidationError(detail=f'invalid parameters: {errs}')

    return res


def get_filter_predicates(
        query_params: Dict[str, Any],
        predicates_map: Dict[str, Callable[[Dict[str, Any], Any], bool]]
) -> List[Callable[[Dict[str, Any]], bool]]:
    """
    TODO
    """
    res = []
    for p_name, p_value in query_params.items():
        res.append(
            lambda dataset, name=p_name, value=p_value: predicates_map[name](dataset, value)
        )
    return res


def filter_item(item: Dict[str, Any],
                predicates: Optional[List[Callable[[Dict[str, Any]], bool]]] = None) -> bool:
    """
    TODO
    """
    if predicates is None:
        return True

    return all([pred(item) for pred in predicates])
