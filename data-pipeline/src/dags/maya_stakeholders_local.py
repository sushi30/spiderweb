from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from models.sql.normalized import Stakeholder
from operators.create_graph_from_sqlite import handler as create_graph_from_sqlite
from operators.normalize_stakeholder_sqlite import (
    handler as normalize_stakeholder_sqlite,
)
from operators.extract_firm_sqlite import handler as extract_firm_sqlite
from operators.normalize_sqlite import handler as normalize_sqlite
from operators.json_stream_to_file import handler as json_stream_to_file
from operators.json_to_sqlite import handler as json_to_sqlite
from models.sql.maya_stakeholder import MayaStakeholder
from models.sql.normalized.firm import Firm
from models.sql.normalized.person import Person


def create_path(path_id, source_url, DbModel):
    create_files = PythonOperator(
        task_id=f"{path_id}_create_files",
        python_callable=json_stream_to_file,
        provide_context=True,
        depends_on_past=False,
        op_kwargs={
            "source_url": source_url,
            "dest_dir": "./artifacts/{{ params.dir_name }}/{{ ts_nodash }}",
        },
    )

    insert_to_sqlite = PythonOperator(
        task_id=f"{path_id}_json_to_sqlite",
        python_callable=json_to_sqlite,
        provide_context=True,
        depends_on_past=False,
        op_kwargs={
            "Model": DbModel,
            "source_dir": "./artifacts/{{ params.dir_name }}/{{ ts_nodash }}",
        },
    )

    normalizers = [
        PythonOperator(
            task_id=f"{path_id}_normalize_{model.__tablename__}",
            python_callable=normalize_sqlite,
            provide_context=True,
            op_kwargs={"SourceModel": DbModel, "TargetModel": model},
        )
        for model in [Firm, Person]
    ]

    extract_firm = PythonOperator(
        task_id=f"extract_firm",
        python_callable=extract_firm_sqlite,
        provide_context=True,
        op_kwargs={"SourceModel": MayaStakeholder},
    )

    normalize_stakeholder = PythonOperator(
        task_id=f"normalize_stakeholder",
        python_callable=normalize_stakeholder_sqlite,
        provide_context=True,
        op_kwargs={"SourceModel": MayaStakeholder},
    )

    create_graph = PythonOperator(
        task_id=f"create_graph_stakeholder",
        python_callable=create_graph_from_sqlite,
        provide_context=True,
        op_kwargs={"SourceModel": Stakeholder},
    )

    create_files >> insert_to_sqlite >> normalizers
    insert_to_sqlite >> extract_firm
    extract_firm >> normalize_stakeholder
    normalizers >> normalize_stakeholder
    normalize_stakeholder >> create_graph


with DAG(
    "maya_stakeholders",
    catchup=True,
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2019, 1, 7),
    schedule_interval="@daily",
    params={"dir_name": "stakeholders"},
    max_active_runs=2,
    default_args={"retries": 0, "depends_on_past": True},
) as dag:
    create_path(
        path_id="maya_stakeholders",
        DbModel=MayaStakeholder,
        source_url="https://next.obudget.org/datapackages/maya/maya_company_stakeholder_list/data/maya_stakeholder_list.json",
    )
