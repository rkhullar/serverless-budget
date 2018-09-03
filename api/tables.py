import boto3
import os

dynamo = boto3.resource('dynamodb')

alias_list = 'budget', 'product', 'order'
env_vars = 'BUDGET_TABLE', 'PRODUCT_TABLE', 'ORDER_TABLE'

tables = {alias: dynamo.Table(os.environ[env_var]) for alias, env_var in zip(alias_list, env_vars)}

budget_table = tables[alias_list[0]]
product_table = tables[alias_list[1]]
order_table = tables[alias_list[2]]
