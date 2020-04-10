from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from operators.json_stream_to_s3 import handler as json_stream_to_s3

with DAG(
    "json_to_document",
    description="Simple tutorial DAG",
    catchup=True,
    start_date=datetime(2019, 1, 1),
    schedule_interval="@once",
) as dag:
    json_to_s3 = PythonOperator(
        task_id="json_to_s3",
        python_callable=json_stream_to_s3,
        provide_context=True,
        op_kwargs={
            "source_url": "https://next.obudget.org/datapackages/maya/maya_company_officer_list/data/maya_company_officer_list.json",
            "dest_bucket_key": None,
            "dest_bucket_name": None,
        },
    )
