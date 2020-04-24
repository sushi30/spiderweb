from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WithTimestamps:
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    @classmethod
    def iterate_rows(cls, session, start_inclusive, end):
        for row in session.query(cls).filter(
            start_inclusive <= cls.created_at, cls.created_at < end
        ):
            yield row


class WithUUID:
    UUID = Column(String(36))

    def get_id(self):
        raise NotImplemented
