from datetime import datetime
import os

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from operators.json_stream_to_file import handler


def print_pwd():
    print(os.getcwd())


with DAG(
    "json_to_document_local",
    catchup=True,
    start_date=datetime(2020, 1, 1),
    schedule_interval="@once",
) as dag:
    json_to_s3 = PythonOperator(
        task_id="json_to_file",
        python_callable=handler,
        provide_context=True,
        op_kwargs={
            "source_url": "https://next.obudget.org/datapackages/maya/maya_company_officer_list/data/maya_company_officer_list.json",
            "dest_dir": "test",
        },
    )
