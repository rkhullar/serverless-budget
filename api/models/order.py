from ..tables import order_table
from typing import NamedTuple, Dict
from decimal import Decimal


class Order(NamedTuple):
    budget_name: str
    product_name: str
    quantity: int

    @staticmethod
    def build_key(budget_name: str, product_name: str) -> Dict:
        return {'budget_name': budget_name, 'product_name': product_name}

    @property
    def primary_key(self) -> Dict:
        return self.build_key(budget_name=self.budget_name, product_name=self.product_name)

    @classmethod
    def load(cls, product_name: str, budget_name: str) -> 'Order':
        response = order_table.get_item(Key=cls.build_key(budget_name, product_name))
        item = response.get('Item')
        if item:
            return cls(**item)

    def delete(self):
        return order_table.delete_item(Key=self.primary_key)

    def update(self, quantity: int = None, more: int = None, less: int = None):
        if quantity is not None:
            return self._update_quantity(value=quantity)
        elif more is not None:
            return self._update_more(value=more)
        elif less is not None:
            return self._update_less(value=less)
        else:
            return self.update(quantity=1)

    def _update_quantity(self, value: int):
        response = order_table.update_item(
            Key=self.primary_key,
            UpdateExpression='set quantity = :x',
            ExpressionAttributeValues={':x': value},
            ReturnValues='UPDATED_NEW'
        )
        return response

    def _update_more(self, value: int):
        response = order_table.update_item(
            Key=self.primary_key,
            UpdateExpression='set quantity = quantity + :x',
            ExpressionAttributeValues={':x': value},
            ReturnValues='UPDATED_NEW'
        )
        return response

    def _update_less(self, value: int):
        response = order_table.update_item(
            Key=self.primary_key,
            UpdateExpression='set quantity = quantity - :x',
            ExpressionAttributeValues={':x': value},
            ReturnValues='UPDATED_NEW'
        )
        return response

    def save(self):
        return self.update(quantity=self.quantity)

    @property
    def product(self) -> 'Product':
        from .product import Product
        return Product.load(self.product_name)

    @property
    def budget(self) -> 'Budget':
        from .budget import Budget
        return Budget.load(self.budget_name)

    @property
    def subtotal(self) -> Decimal:
        return self.product.unit_price * self.quantity
