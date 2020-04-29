from uuid import UUID
from sqlalchemy import Column, Float, String, Integer, Date, DateTime, Text
from .firm import Firm
from .person import Person
from .. import Base, WithTimestamps, WithUUID
from ..constants import ID_TYPE_DICT
from ..db_model import DbModel
from ..maya_stakeholder import MayaStakeholder

NAME_SPACE = UUID("269d4861-7b66-43bd-b4b7-43a7c12e554c")


class Stakeholder(WithTimestamps, DbModel, Base):
    __tablename__ = "stakeholders"

    HOLDER = Column(String(36), nullable=False, primary_key=True)
    FIRM = Column(String(36), nullable=False, primary_key=True)
    CAPITAL_PERCENT = Column(Float)
    NUM_STOCKS = Column(Integer)
    DATE = Column(Date)
    NOTES = Column(Text)
    created_at = Column(DateTime, nullable=False, primary_key=True)

    @classmethod
    def from_source(cls, row: MayaStakeholder, session=None, **kwargs):
        if row.__class__.__name__ == "MayaStakeholder":
            holder: WithUUID = session.query(Firm).get(
                (row.MisparZihui, ID_TYPE_DICT[row.SugMisparZihui])
            )
            if holder is None:
                holder = session.query(Person).get(
                    (row.MisparZihui, ID_TYPE_DICT[row.SugMisparZihui])
                )
            if holder is None:
                raise Exception(
                    "Not Found: " + str((row.MisparZihui, row.SugMisparZihui))
                )
            firm = session.query(Firm).get(
                (row.HeaderMisparBaRasham, "israeli_company_registrar")
            )
            return cls(
                **dict(
                    HOLDER=holder.UUID,
                    FIRM=firm.UUID,
                    CAPITAL_PERCENT=row.CapitalPct,
                    NUM_STOCKS=row.CurrentAmount,
                    DATE=row.Date2,
                    NOTES=row.Notes,
                ),
                **kwargs
            )
        else:
            raise Exception("unknown source: " + row.__class__.__name__)
