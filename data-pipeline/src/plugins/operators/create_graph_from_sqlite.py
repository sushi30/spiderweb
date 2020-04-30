from airflow.hooks.sqlite_hook import SqliteHook
import neomodel
from sqlalchemy.orm import sessionmaker
from models.sql.normalized import (
    Firm as SqlFirm,
    Person as SqlPerson,
    Stakeholder as SqlStakeholder,
)
from models.neo4j import Firm as GraphFirm
from utils.handlers import iteration_handler


def get_holder(session, row):
    holder = session.query(SqlFirm).filter_by(UUID=row.HOLDER).one_or_none()
    if holder is None:
        holder = session.query(SqlPerson).filter_by(UUID=row.HOLDER).one_or_none()
    return holder


def process_record(session, execution_date, row: SqlStakeholder):
    sql_firm: SqlFirm = session.query(SqlFirm).filter_by(UUID=row.FIRM).one_or_none()
    # sql_holder = get_holder(session, row)
    GraphFirm.create_or_update(
        name=sql_firm.HEBREW_NAME or sql_firm.ENGLISH_NAME,
        uuid=sql_firm.UUID,
        created_at=execution_date,
    )


def handler(SourceModel, next_execution_date, execution_date, **kwargs):
    connection = SqliteHook()
    Session = sessionmaker(
        bind=connection.get_sqlalchemy_engine(), expire_on_commit=False
    )
    neomodel.db.set_connection("bolt://neo4j:neo4j@neo4j:7687")
    session = Session()
    return iteration_handler(
        SourceModel.iterate_rows(Session(), execution_date, next_execution_date),
        lambda x: process_record(session, execution_date, x),
    )
