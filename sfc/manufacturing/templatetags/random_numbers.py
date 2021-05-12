import random
from django import template

register = template.Library()

@register.simple_tag
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)


import random

def generate(unique):
    chars = "1234567890"
    while True:
        value = "".join(random.choice(chars) for _ in range(6))
        if value not in unique:
            unique.add(value)
            break

unique = set()
for _ in range(10):
    generate(unique)


#####################################
from random import randint
@register.simple_tag
def random_number(length=6):
    return randint(10 ** (length - 1), (10 ** (length) - 1))
