from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from operators.json_stream_to_files import handler as json_stream_to_files

with DAG(
    dag_id="maya_stakeholders_read_json_stream",
    catchup=True,
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2019, 4, 1),
    schedule_interval="@once",
    params={"dir_name": "stakeholders"},
    max_active_runs=2,
    default_args={"retries": 0, "depends_on_past": True},
) as dag:
    create_files = PythonOperator(
        retries=3,
        task_id=f"maya_stakeholders_create_files",
        python_callable=json_stream_to_files,
        provide_context=True,
        depends_on_past=False,
        op_kwargs={
            "source_url": "https://next.obudget.org/datapackages/maya/maya_company_stakeholder_list/data/maya_stakeholder_list.json",
            "dest_dir": "./artifacts/{{ params.dir_name }}",
        },
    )
