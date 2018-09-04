from typing import Dict
import json


def build_response(data: Dict=dict(), status: int=200, encoded: bool=False, headers: Dict=dict(), **kwargs):
    combined = {**data, **kwargs}
    return dict(body=json.dumps(combined), statusCode=status, headers=headers, isBase64Encoded=encoded)


def handler(event, context):
    method, path = event.get('httpMethod').lower(), event.get('path')
    response = build_response(
        message='hello world', method=method, path=path,
        path_params=event.get('pathParameters'),
        body=json.loads(event.get('body') or '{}')
        )
    return response
