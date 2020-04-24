from datetime import datetime
import json
from logging import warning
import os
import traceback
from airflow.hooks.sqlite_hook import SqliteHook
from sqlalchemy.orm import sessionmaker
from models.sql import DbModel


def process_record(session, execution_date, Model: DbModel, file_content):
    record = json.loads(file_content)
    model = Model.from_dict(
        record, created_at=execution_date, updated_at=datetime.utcnow()
    )
    try:
        model.insert_or_update(session)
    except Exception as err:
        warning(err)
        session.rollback()
        pass


def handler(source_dir, Model, execution_date, **kwargs):
    files = os.listdir(source_dir)
    connection = SqliteHook()
    Session = sessionmaker(bind=connection.get_sqlalchemy_engine())
    session = Session()
    for file in files:
        with open(os.path.join(source_dir, file), encoding="utf8") as fp:
            try:
                process_record(session, execution_date, Model, fp.read())
            except:
                traceback.print_exc()
                pass
