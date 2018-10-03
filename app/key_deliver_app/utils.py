import string as s
import random as r


DEFAULT_KEY_SIZE = 4
KEY_PIECES = s.ascii_letters + s.digits


def generate_value(size=DEFAULT_KEY_SIZE):
    return ''.join(r.choice(KEY_PIECES) for _ in range(size))
