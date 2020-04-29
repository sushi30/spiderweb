from datetime import datetime
import json
from logging import warning
import os
from airflow.hooks.sqlite_hook import SqliteHook
from sqlalchemy.orm import sessionmaker
from models.sql.db_model import DbModel
from utils.handlers import iteration_handler


def process_record(session, execution_date, Model: DbModel, path):
    with open(path, encoding="utf8") as fp:
        record = json.load(fp)
        model = Model.from_dict(
            record, created_at=execution_date, updated_at=datetime.utcnow()
        )
        model.insert_or_update(session)


def handler(source_dir, Model, execution_date, **kwargs):
    connection = SqliteHook()
    Session = sessionmaker(bind=connection.get_sqlalchemy_engine())
    session = Session()

    def handle_error(file_path):
        session.rollback()
        warning(file_path)

    return iteration_handler(
        os.listdir(source_dir),
        lambda x: process_record(
            session, execution_date, Model, os.path.join(source_dir, x)
        ),
        handle_error,
    )
