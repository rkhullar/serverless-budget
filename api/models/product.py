from ..tables import product_table

from typing import NamedTuple, Dict
from decimal import Decimal


class Product(NamedTuple):
    name: str
    unit_price: Decimal

    @staticmethod
    def build_key(name: str) -> Dict:
        return {'name': name}

    @property
    def primary_key(self) -> Dict:
        return self.build_key(name=self.name)

    @classmethod
    def load(cls, name: str) -> 'Product':
        response = product_table.get_item(Key=cls.build_key(name))
        item = response.get('Item')
        if item:
            return cls(**item)

    def update(self, **data):
        response = product_table.update_item(
            Key=self.primary_key,
            UpdateExpression='set' + ' ' + ', '.join(f'{key}=:{key}' for key in data.keys()),
            ExpressionAttributeValues={f':{key}': value for key, value in data.items()},
            ReturnValues='UPDATED_NEW'
        )
        return response

    def save(self):
        return self.update(unit_price=self.unit_price)

    def delete(self):
        return product_table.delete_item(Key=self.primary_key)
