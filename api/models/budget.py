from ..tables import budget_table, order_table
from .order import Order

from boto3.dynamodb.conditions import Key
from typing import NamedTuple, Dict, List
from decimal import Decimal


class Budget(NamedTuple):
    name: str

    @staticmethod
    def build_key(name: str) -> Dict:
        return {'name': name}

    @property
    def primary_key(self) -> Dict:
        return self.build_key(name=self.name)

    @classmethod
    def load(cls, name: str) -> 'Budget':
        response = budget_table.get_item(Key=cls.build_key(name))
        item = response.get('Item')
        if item:
            return cls(**item)

    def delete(self):
        response = budget_table.delete_item(Key={'name': self.name})
        return response

    def update(self, **data):
        if data:
            response = budget_table.update_item(
                Key=self.primary_key,
                UpdateExpression='set' + ' ' + ', '.join(f'{key}=:{key}' for key in data.keys()),
                ExpressionAttributeValues={f':{key}': value for key, value in data.items()},
                ReturnValues='UPDATED_NEW'
            )
            return response
        else:
            return budget_table.put_item(Item=self.primary_key)

    def save(self):
        return self.update()

    @property
    def orders(self) -> List['Order']:
        response = order_table.query(KeyConditionExpression=Key('budget_name').eq(self.name))
        items = response.get('Items', [])
        return [Order(**item) for item in items]

    def clear(self):
        response = order_table.query(KeyConditionExpression=Key('budget_name').eq(self.name))
        items = response.get('Items', [])
        for item in items:
            order = Order(**item)
            order.delete()

    @staticmethod
    def read() -> List['Budget']:
        response = budget_table.scan()
        items = response.get('Items', [])
        return [Budget(**item) for item in items]

    @property
    def total(self) -> Decimal:
        result = Decimal(0)
        for order in self.orders:
            result += order.subtotal
        return result
