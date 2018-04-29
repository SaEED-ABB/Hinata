from django.utils.crypto import get_random_string


def get_path(instance, filename):
    name = get_random_string(length=24) + "." + filename.split('.')[-1]
    return "images/" + name
