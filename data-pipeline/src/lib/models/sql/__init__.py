from sqlalchemy import Column, DateTime, String, inspect
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DbModel:
    def get_identifier(self):
        pk = tuple([c.name for c in inspect(self.__class__).primary_key])
        return tuple([self.__getattribute__(col) for col in pk])

    def update_columns(self):
        pk = set([c.name for c in inspect(self.__class__).primary_key])
        columns = set([c.name for c in inspect(self.__class__).columns])
        return list(columns - pk)

    def insert_or_update(self, session):
        existing = session.query(self.__class__).get(row.get_identifier())
        if existing is None:
            session.add(self)
        else:
            for column in self.update_columns():
                existing.__setattr__(column, self.__getattribute__(column))
        session.commit()

    def from_dict(self, d: dict, **kwargs):
        raise NotImplemented

    @classmethod
    def from_source(cls, model, row: Base, **kwargs):
        return None

    @classmethod
    def infer_type(cls, row: "DbModel"):
        return False


class WithTimestamps:
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class WithUUID:
    UUID = Column(String(36))

    def get_id(self):
        raise NotImplemented
