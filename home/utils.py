# utils.py
import hashlib
import time

def get_filename(filename, request):
    hash_object = hashlib.sha1(str(time.time()).encode('utf-8'))
    hash_object.update(filename.encode('utf-8'))
    return f'{hash_object.hexdigest()[:10]}-{filename}'
