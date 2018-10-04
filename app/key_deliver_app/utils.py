import string as s
import random as r

from key_deliver_app.models import Key


DEFAULT_KEY_SIZE = 4
KEY_PIECES = s.ascii_letters + s.digits


def generate_random_value(size=DEFAULT_KEY_SIZE):
    return ''.join(r.choice(KEY_PIECES) for _ in range(size))


def generate_unique_key_value():
    value = generate_random_value()
    return value if not Key.objects.filter(value=value).exists() \
        else generate_random_value()
