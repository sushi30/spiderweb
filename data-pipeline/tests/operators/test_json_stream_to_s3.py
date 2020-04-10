from datetime import datetime, timedelta
import requests
from dags.operators.json_stream import json_stream_from_request


def test_stream_from_real_source():
    source_url = "https://next.obudget.org/datapackages/maya/maya_company_officer_list/data/maya_company_officer_list.json"
    execution_date = datetime(2019, 1, 1)
    prev_execution_date = None
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
