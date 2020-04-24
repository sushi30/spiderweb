from hashlib import md5
from datetime import datetime, timedelta
import json
import os

import requests
from utils.json_stream import json_stream_from_request


def hash_json(o):
    h = md5()
    h.update(json.dumps(o).encode(encoding="utf8"))
    return h.hexdigest()


def handler(source_url, dest_dir, execution_date, prev_execution_date, **kwags):
    r = requests.get(source_url, stream=True)
    prev_execution_date = prev_execution_date or (execution_date - timedelta(days=1))
    max_date = datetime(1900, 1, 1)
    min_date = datetime(2100, 1, 1)
    success = 0
    for o in json_stream_from_request(r):
        date = datetime.fromisoformat(o["date"])
        if date > max_date:
            print("max_date", date)
            max_date = date
        if date < min_date:
            print("min_date", date)
            min_date = date
        if execution_date < date:
            continue
        elif prev_execution_date < date < execution_date:
            print("writing date", date)
            os.makedirs(dest_dir, exist_ok=True)
            h = hash_json(o)
            with open(os.path.join(dest_dir, h + ".json"), "w") as fp:
                json.dump(o, fp, ensure_ascii=False)
            success += 1
        elif date < prev_execution_date - timedelta(days=365):
            break
        else:
            continue
        return success
