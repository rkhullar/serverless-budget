from typing import Dict
import json


def build_response(data: Dict=None, status: int=200, encoded: bool=False, headers: Dict=None, **kwargs):
    combined = {**(data or dict()), **kwargs}
    return dict(body=json.dumps(combined), statusCode=status, headers=headers or dict(), isBase64Encoded=encoded)


def handler(event, context):
    method = event['httpMethod'].lower()
    resource, path, path_params = map(event.get, ['resource', 'path', 'pathParameters'])
    body = json.loads(event.get('body') or '{}')

    data = {}

    if resource == '/products':
        if method == 'get':
            data['message'] = "returning all products"

        elif method == 'put':
            data['message'] = "creating new product"
            data['name'] = body['name']
            data['unit_price'] = body['unit_price']

    elif resource == '/budgets':
        if method == 'get':
            data['message'] = "returning all budgets"

        elif method == 'put':
            data['message'] = "creating new budget"
            data['name'] = body['name']

    elif resource == '/products/{name+}':
        data['name'] = path_params['name']

        if method == 'get':
            data['message'] = "returning product detail"

        elif method == 'delete':
            data['message'] = "deleting product"

    elif resource == '/budgets/{name+}':
        data['name'] = path_params['name']

        if method == 'get':
            data['message'] = "returning budget detail"

        elif method == 'delete':
            data['message'] = "deleting budget"

    return build_response(data)
