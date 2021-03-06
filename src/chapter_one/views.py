from typing import Any, Dict, Optional, List
from functools import partial

from django.conf import settings
from django.views.decorators.cache import cache_page

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import exceptions

from . import views_utils


fetch_json = partial(views_utils.fetch_json,
                     timeout=settings.CHAPTER_ONE['EXTERNAL_REQUEST_TIMEOUT_SEC'],
                     cache_timeout=settings.CHAPTER_ONE['CACHE_TIMEOUT_SEC'])


def _convert_recipient_format(external_recipient: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'surname': external_recipient['info']['surname'],
        'name': external_recipient['info']['name'],
        'patronymic': external_recipient['info']['patronymic'],
        'phoneNumber': external_recipient['contacts']['phoneNumber'],
    }


@cache_page(settings.CHAPTER_ONE['CACHE_TIMEOUT_SEC'])
@api_view(http_method_names=['GET'])
def recipients(_: Request) -> Response:
    recipients_json = fetch_json(settings.CHAPTER_ONE['RECIPIENTS_URL'])
    try:
        return Response([_convert_recipient_format(r) for r in recipients_json])
    except KeyError:
        raise exceptions.APIException(detail='unexpected recipients external format')


def _get_recipient_by_id(recipients_json: List[Dict[str, Any]], pk: int) -> Optional[Dict[str, Any]]:
    """
    I don't know what is `id`, so let's take sequence number (index) as `id` (just as workaround)
    https://stepik.org/lesson/370334/step/2?unit=355780
    """
    try:
        return recipients_json[pk-1]
    except IndexError:
        return


@cache_page(settings.CHAPTER_ONE['CACHE_TIMEOUT_SEC'])
@api_view(http_method_names=['GET'])
def recipient(_: Request, pk: int) -> Response:
    recipients_json = fetch_json(settings.CHAPTER_ONE['RECIPIENTS_URL'])

    recipient_json = _get_recipient_by_id(recipients_json, pk)
    if recipient_json is None:
        raise exceptions.NotFound()

    try:
        return Response(_convert_recipient_format(recipient_json))
    except KeyError:
        raise exceptions.APIException(detail='unexpected recipient external format')


# ---
DATASET_PREDICATES_MAP = {
    'min_price': lambda dataset, price: dataset['price'] >= price,
    'min_weight': lambda dataset, weight: dataset['weight'] >= weight,
}
DATASET_PARAM_GETTER_MAP = {
    'min_price': lambda query_dict: views_utils.get_min_from_query_dict_by_key(query_dict, 'min_price'),
    'min_weight': lambda query_dict: views_utils.get_min_from_query_dict_by_key(query_dict, 'min_weight'),
}


def _convert_dataset_format(external_dataset: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'title': external_dataset['name'],
        'description': external_dataset['about'],
        'price': external_dataset['price'],
        'weight': external_dataset['weight_grams'],
    }


@api_view(http_method_names=['GET'])
def product_sets(request: Request) -> Response:
    query_params = views_utils.get_query_params(request.query_params, DATASET_PARAM_GETTER_MAP)
    datasets_json = fetch_json(settings.CHAPTER_ONE['DATASET_URL'])

    res = []
    filter_predicates = views_utils.get_filter_predicates(query_params, DATASET_PREDICATES_MAP)
    for dataset in datasets_json:
        try:
            product = _convert_dataset_format(dataset)
        except KeyError:
            raise exceptions.APIException(detail='unexpected products external format')

        if views_utils.filter_item(product, filter_predicates):
            res.append(product)
    # TODO: cache by query params
    return Response(res)


def _get_dataset_by_id(datasets_json: List[Dict[str, Any]], pk: int) -> Optional[Dict[str, Any]]:
    """
    I don't know what is `id`, so let's take `inner_id` as `id` (just as workaround)
    https://stepik.org/lesson/370334/step/2?unit=355780
    """
    for d_j in datasets_json:
        try:
            if d_j['inner_id'] == pk:
                return d_j
        except KeyError:
            return


@cache_page(settings.CHAPTER_ONE['CACHE_TIMEOUT_SEC'])
@api_view(http_method_names=['GET'])
def product_set(_: Request, pk: int) -> Response:
    datasets_json = fetch_json(settings.CHAPTER_ONE['DATASET_URL'])

    dataset_json = _get_dataset_by_id(datasets_json, pk)
    if dataset_json is None:
        raise exceptions.NotFound()

    try:
        return Response(_convert_dataset_format(dataset_json))
    except KeyError:
        raise exceptions.APIException(detail='unexpected products external format')
