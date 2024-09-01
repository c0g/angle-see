import itertools
import re
import os
import json
import io
import litellm
from dotenv import load_dotenv
import base64

from tqdm import tqdm
from angle_see.generate_simple_angle import generate_line_intersection_image
import diskcache as dc
import pickle

load_dotenv()  # take environment variables from .env.

def encode_image(image):
    f = io.BytesIO()
    image.save(f, format="PNG")
    f.flush()
    return base64.b64encode(f.getvalue())

def recurse_dict(thing):
    try:
        json.dumps(thing)
        return thing
    except:
        as_dict = dict(thing)
        return {k: recurse_dict(v) for k, v in as_dict.items()}


cache = dc.Cache(".cache")

def cached_completion(model, messages, temp, rep):
    key = json.dumps(
        {"model": model, "messages": messages, "temp": temp, "rep": rep}, sort_keys=True
    ).encode()
    if key not in cache:
        response = litellm.completion(
            model=model, messages=messages, temperature=temp
        )
        cache[key] = json.dumps(response.to_dict())
    return json.loads(cache[key])