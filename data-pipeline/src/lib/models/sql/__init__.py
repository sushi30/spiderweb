from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WithTimestamps:
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class WithUUID:
    UUID = Column(String(36))

    def get_id(self):
        raise NotImplemented
