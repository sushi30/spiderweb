from datetime import datetime
from airflow.hooks.sqlite_hook import SqliteHook
from sqlalchemy.orm import sessionmaker
from models.sql.normalized import Stakeholder
from utils.handlers import iteration_handler


def process_record(session, execution_date, row):
    Stakeholder.from_source(
        row, session, created_at=execution_date, updated_at=datetime.utcnow()
    ).insert_or_update(session)


def handler(SourceModel, execution_date, next_execution_date, **kwargs):
    connection = SqliteHook()
    Session = sessionmaker(
        bind=connection.get_sqlalchemy_engine(), expire_on_commit=False
    )
    session = Session()

    def handle_error(*_, **__):
        session.rollback()

    return iteration_handler(
        SourceModel.iterate_rows(Session(), execution_date, next_execution_date),
        lambda x: process_record(session, execution_date, x),
        handle_error,
    )
