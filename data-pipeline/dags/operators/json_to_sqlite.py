import json
import os
from airflow.hooks.sqlite_hook import SqliteHook
from sqlalchemy.orm import sessionmaker


def add_rows(session, rows):
    try:
        session.add_all(rows)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def handler(source_dir, Model, execution_date, **kwargs):
    files = os.listdir(source_dir)
    records = []
    for file in files:
        with open(os.path.join(source_dir, file), encoding="utf8") as fp:
            records.append(json.load(fp))
    items = [Model.from_dict(**r, created_at=execution_date) for r in records]
    connection = SqliteHook()
    print(connection.get_uri())
    Session = sessionmaker(bind=connection.get_sqlalchemy_engine())
    add_rows(Session(), items)
