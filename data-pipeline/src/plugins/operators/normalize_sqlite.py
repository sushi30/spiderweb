from datetime import datetime, timedelta
from airflow.hooks.sqlite_hook import SqliteHook
from sqlalchemy.orm import sessionmaker
from models.sql.db_model import DbModel
from utils.handlers import iteration_handler


def process_record(session, execution_date, TargetModel: DbModel, row):
    if TargetModel.infer_type(row):
        TargetModel.from_source(
            row, created_at=execution_date, updated_at=datetime.utcnow()
        ).insert_or_update(session)


def handler(SourceModel, TargetModel, prev_execution_date, execution_date, **kwargs):
    prev_execution_date = prev_execution_date or (execution_date - timedelta(days=1))
    connection = SqliteHook()
    Session = sessionmaker(
        bind=connection.get_sqlalchemy_engine(), expire_on_commit=False
    )
    session = Session()
    return iteration_handler(
        SourceModel.iterate_rows(Session(), prev_execution_date, execution_date),
        lambda x: process_record(session, execution_date, TargetModel, x),
        session.rollback,
    )
