from datetime import datetime

from airflow.hooks.sqlite_hook import SqliteHook
import neomodel
from sqlalchemy.orm import sessionmaker
from models.sql.normalized import (
    Firm as SqlFirm,
    Person as SqlPerson,
    Stakeholder as SqlStakeholder,
)
from models.neo4j import Firm as GraphFirm, Person as GraphPerson, StakeholderRel
from utils.handlers import iteration_handler


def date_to_datetime(date):
    return datetime.combine(date, datetime.min.time())


def get_holder(session, row):
    holder = session.query(SqlFirm).filter_by(UUID=row.HOLDER).one_or_none()
    if holder is None:
        holder = session.query(SqlPerson).filter_by(UUID=row.HOLDER).one_or_none()
    return holder


def process_record(session, execution_date, row: SqlStakeholder):
    sql_firm: SqlFirm = session.query(SqlFirm).filter_by(UUID=row.FIRM).one_or_none()
    sql_holder = get_holder(session, row)
    execution_datetime = date_to_datetime(execution_date)
    graph_firm = GraphFirm.create_or_update(
        name=sql_firm.HEBREW_NAME or sql_firm.ENGLISH_NAME,
        uuid=sql_firm.UUID,
        created_at=execution_datetime,
    )
    if sql_holder.__class__ == SqlFirm:
        graph_holder = GraphFirm.create_or_update(
            name=sql_holder.HEBREW_NAME or sql_holder.ENGLISH_NAME,
            uuid=sql_holder.UUID,
            created_at=execution_datetime,
        )
    elif sql_holder.__class__ == SqlPerson:
        graph_holder = GraphPerson.create_or_update(
            name=sql_holder.HEBREW_NAME or sql_holder.ENGLISH_NAME,
            uuid=sql_holder.UUID,
            created_at=execution_datetime,
        )
    else:
        raise Exception("unknown type: " + str(sql_holder.__class__))
    existing_relationship: StakeholderRel = graph_firm.stakeholder.relationship(
        graph_holder
    )
    if existing_relationship is None:
        graph_firm.stakeholder.connect(
            graph_holder,
            {
                "capital_percent": row.CAPITAL_PERCENT,
                "date": date_to_datetime(row.DATE),
                "stock_amount": row.NUM_STOCKS,
                "notes": row.NOTES,
                "created_at": execution_datetime,
            },
        )
    elif existing_relationship.date < date_to_datetime(row.DATE):
        existing_relationship.capital_percent = row.CAPITAL_PERCENT
        existing_relationship.date = row.DATE
        existing_relationship.notes = row.NOTES
        existing_relationship.stock_amount = row.NUM_STOCKS
        existing_relationship.created_at = row.created_at
        existing_relationship.updated_at = datetime.now()
        existing_relationship.save()


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
