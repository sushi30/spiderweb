from datetime import datetime, timedelta
from logging import warning
from typing import List
from airflow.hooks.sqlite_hook import SqliteHook
from sqlalchemy.orm import sessionmaker
from models.sql import WithTimestamps
from models.sql.normalized.firm import Firm
from utils.handlers import iteration_handler


def process_record(session, execution_date, row):
    try:
        Firm.extract_firm(
            row, created_at=execution_date, updated_at=datetime.utcnow()
        ).insert_or_update(session)
    except Exception as err:
        warning(err)
        session.rollback()
        pass


def handler(SourceModel: WithTimestamps, prev_execution_date, execution_date, **kwargs):
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
