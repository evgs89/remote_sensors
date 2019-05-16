import random
import string


def id_generator(size = 12, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
