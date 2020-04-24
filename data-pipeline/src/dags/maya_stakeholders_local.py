from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from operators.normalize_sqlite import handler as normalize_sqlite
from operators.json_stream_to_file import handler as json_stream_to_file
from operators.json_to_sqlite import handler as json_to_sqlite
from models.sql.maya_stakeholders import MayaStakeholder
from models.sql.normalized.firm import Firm
from models.sql.normalized.person import Person


def create_path(path_id, source_url, DbModel):
    create_files = PythonOperator(
        task_id=f"{path_id}_create_files",
        python_callable=json_stream_to_file,
        provide_context=True,
        op_kwargs={
            "source_url": source_url,
            "dest_dir": "./artifacts/{{ params.dir_name }}/{{ ts_nodash }}",
        },
    )

    insert_to_sqlite = PythonOperator(
        task_id=f"{path_id}_json_to_sqlite",
        python_callable=json_to_sqlite,
        provide_context=True,
        op_kwargs={
            "Model": DbModel,
            "source_dir": "./artifacts/{{ params.dir_name }}/{{ ts_nodash }}",
        },
    )

    normalizers = [
        PythonOperator(
            task_concurrency=2,
            retries=3,
            task_id=f"{path_id}_normalize_{model.__tablename__}",
            python_callable=normalize_sqlite,
            provide_context=True,
            op_kwargs={"SourceModel": DbModel, "TargetModel": model},
        )
        for model in [Firm, Person]
    ]

    create_files >> insert_to_sqlite >> normalizers


with DAG(
    "maya_stakeholders",
    catchup=True,
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2019, 1, 7),
    schedule_interval="@daily",
    max_active_runs=2,
    params={"dir_name": "stakeholders"},
    concurrency=2,
) as dag:
    create_path(
        path_id="maya_stakeholders",
        DbModel=MayaStakeholder,
        source_url="https://next.obudget.org/datapackages/maya/maya_company_stakeholder_list/data/maya_stakeholder_list.json",
    )