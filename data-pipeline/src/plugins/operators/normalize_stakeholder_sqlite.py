from datetime import datetime, timedelta
from airflow.hooks.sqlite_hook import SqliteHook
from sqlalchemy.orm import sessionmaker
from models.sql.normalized import Stakeholder
from utils.handlers import iteration_handler


def process_record(session, execution_date, row):
    Stakeholder.from_source(
        row, session, created_at=execution_date, updated_at=datetime.utcnow()
    ).insert_or_update(session)


def handler(SourceModel, prev_execution_date, execution_date, **kwargs):
    prev_execution_date = prev_execution_date or (execution_date - timedelta(days=1))
    connection = SqliteHook()
    Session = sessionmaker(
        bind=connection.get_sqlalchemy_engine(), expire_on_commit=False
    )
    session = Session()
    return iteration_handler(
        SourceModel.iterate_rows(Session(), prev_execution_date, execution_date),
        lambda x: process_record(session, execution_date, x),
        session.rollback,
    )
