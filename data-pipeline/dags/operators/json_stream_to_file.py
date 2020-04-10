from hashlib import md5
from datetime import datetime, timedelta
import json
import os

import requests
from operators.json_stream import json_stream_from_request


def hash_json(o):
    h = md5()
    h.update(json.dumps(o).encode(encoding="utf8"))
    return h.hexdigest()


def handler(source_url, dest_dir, execution_date, prev_execution_date, **kwags):
    r = requests.get(source_url, stream=True)
    prev_execution_date = prev_execution_date or (execution_date - timedelta(days=1))
    for o in json_stream_from_request(r):
        date = datetime.fromisoformat(o["date"])
        if execution_date < date:
            continue
        elif prev_execution_date < date < execution_date:
            os.makedirs(f"./artifacts/{dest_dir}", exist_ok=True)
            h = hash_json(o)
            with open(f"./artifacts/{dest_dir}/{h}.json", "w") as fp:
                json.dump(o, fp)
        else:
            continue
