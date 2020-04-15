from datetime import datetime
import requests
from utils.json_stream import json_stream_from_request


def test_stream_from_real_source_officers():
    r = requests.get(
        "https://next.obudget.org/datapackages/maya/maya_company_officer_list/data/maya_company_officer_list.json",
        stream=True,
    )
    for o in json_stream_from_request(r, buffer_size=256):
        date = datetime.fromisoformat(o["date"])
        if datetime(2019, 12, 1) < date < datetime(2020, 1, 1):
            print(o)
        elif date < datetime(2019, 1, 1):
            break


def test_stream_from_real_source_stakeholders():
    r = requests.get(
        "https://next.obudget.org/datapackages/maya/maya_company_stakeholder_list/data/maya_stakeholder_list.json",
        stream=True,
    )
    for o in json_stream_from_request(r):
        date = datetime.fromisoformat(o["date"])
        if datetime(2018, 12, 31) < date < datetime(2019, 1, 1):
            print(o)
        else:
            break
