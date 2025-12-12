from django import template
register = template.Library()

@register.simple_tag(name='my_connection')
def my_connection(table: str, column: str) -> str:
    return f"CONNECTION TO {table.upper()} ON COLUMN {column.upper()}"

@register.filter(name='my_name')
def name(value: str) -> str:
    if(value):
        return f"Name: {value}"
    
    return f"Sin Nombre"

@register.filter(name='my_complete_name')
def name(name: str, surname: str) -> str:
    return f"COMPLETE NAME: {name} {surname}"

@register.filter(name='my_complete_info')
def name(value: str, surname: str, age:str) -> str:
    return f"COMPLETE NAME: {value} {surname} {age}"

    