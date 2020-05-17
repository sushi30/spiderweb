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


def handler(SourceModel, TargetModel, execution_date, next_execution_date, **kwargs):
    connection = SqliteHook()
    Session = sessionmaker(
        bind=connection.get_sqlalchemy_engine(), expire_on_commit=False
    )
    session = Session()

    def handle_error(*_, **__):
        session.rollback()

    return iteration_handler(
        SourceModel.iterate_rows(Session(), execution_date, next_execution_date),
        lambda x: process_record(session, execution_date, TargetModel, x),
        handle_error,
    )
