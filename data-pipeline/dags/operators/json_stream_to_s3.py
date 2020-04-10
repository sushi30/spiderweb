from datetime import datetime, timedelta

import boto3
import requests
from operators.json_stream import json_stream_from_request


def upload_to_s3(body, bucket, key):
    return boto3.resource("s3").Object(bucket, key).put(Body=body)


def handler(
    source_url,
    dest_bucket_key,
    dest_bucket_name,
    ts,
    execution_date,
    prev_execution_date,
    **kwags,
):
    r = requests.get(source_url, stream=True)
    prev_execution_date = prev_execution_date or (execution_date - timedelta(days=1))
    for o in json_stream_from_request(r):
        date = datetime.fromisoformat(o["date"])
        if execution_date < date:
            continue
        elif prev_execution_date < date < execution_date:
            print(o)
        else:
            continue
