import pytest
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sql.db_model import DbModel

Base = declarative_base()


class Animal(DbModel, Base):
    __tablename__ = "animal"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))


@pytest.fixture
def sqlite_engine():
    return create_engine("sqlite://")


@pytest.fixture
def mock_tables(session, sqlite_engine):
    Base.metadata.create_all(bind=sqlite_engine)
    session.add(Animal(id=1, name="cat"))
    session.add(Animal(id=2, name="dog"))


@pytest.fixture
def session(sqlite_engine):
    return sessionmaker(bind=sqlite_engine)()


def test_add_row_ignore_duplicate(session, mock_tables):
    Animal(id=1, name="lion").insert_or_update(session)
    Animal(id=3, name="giraffe").insert_or_update(session)
    assert session.query(Animal).filter_by(id=1)[0].name == "lion"
    assert session.query(Animal).filter_by(id=3)[0].name == "giraffe"
