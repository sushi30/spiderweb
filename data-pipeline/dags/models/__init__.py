from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WtihTimestamps:
    created_at = Column(DateTime, server_default=func.utc_timestamp())
    updated_at = Column(DateTime, onupdate=func.utc_timestamp())
