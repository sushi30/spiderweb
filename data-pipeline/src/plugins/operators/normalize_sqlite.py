from datetime import datetime, timedelta
from logging import warning
from typing import List
from airflow.hooks.sqlite_hook import SqliteHook
from sqlalchemy.orm import sessionmaker
from models.sql.db_model import DbModel


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
    rows: List[DbModel] = (
        Session()
        .query(SourceModel)
        .filter(
            prev_execution_date <= SourceModel.created_at,
            SourceModel.created_at < execution_date,
        )
    )
    session = Session()
    success = 0
    for row in rows:
        try:
            process_record(session, execution_date, TargetModel, row)
            success += 1
        except Exception as err:
            warning(err)
            session.rollback()
    session.close()
    return f"{success}/{len(rows)}"
