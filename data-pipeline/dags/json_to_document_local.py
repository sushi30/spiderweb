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
    end_date=datetime(2020, 1, 3),
    schedule_interval="@daily",
) as dag:
    maya_company_officer_list = PythonOperator(
        task_id="maya_company_officer_list",
        python_callable=handler,
        provide_context=True,
        op_kwargs={
            "source_url": "https://next.obudget.org/datapackages/maya/maya_company_officer_list/data/maya_company_officer_list.json",
            "dest_dir": "officers",
        },
    )

    maya_stakeholder_list = PythonOperator(
        task_id="maya_stakeholder_list",
        python_callable=handler,
        provide_context=True,
        op_kwargs={
            "source_url": "https://next.obudget.org/datapackages/maya/maya_company_stakeholder_list/data/maya_stakeholder_list.json",
            "dest_dir": "stakeholders",
        },
    )


