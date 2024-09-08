import base64
import io
import json
import time

import diskcache as dc
import litellm
from dotenv import load_dotenv

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
    except Exception:
        as_dict = dict(thing)
        return {k: recurse_dict(v) for k, v in as_dict.items()}


cache = dc.Cache(".cache")


def cached_completion(model, messages, temp, rep):
    key = json.dumps(
        {"model": model, "messages": messages, "temp": temp, "rep": rep}, sort_keys=True
    ).encode()
    if key not in cache:
        # print(key)
        # re-try back off
        for i in range(5):
            try:
                response = litellm.completion(model=model, messages=messages, temperature=temp)
                cache[key] = json.dumps(response.to_dict())
                break
            except Exception as e:
                print(e)
                time.sleep(0.1)
        else:
            raise Exception("Failed to cache completion")
    return json.loads(cache[key])
