from uuid import UUID, uuid5

from sqlalchemy import Column, String

from .. import Base, WithUUID, WithTimestamps
from ..constants import ID_TYPE_DICT
from ..db_model import DbModel
from ..maya_stakeholder import MayaStakeholder

NAME_SPACE = UUID("{45690d8b-71e7-45a1-9518-2a8e66df3b18}")


class Person(WithTimestamps, WithUUID, DbModel, Base):
    __tablename__ = "person"

    HEBREW_NAME = Column(String)
    ENGLISH_NAME = Column(String)
    ID = Column(String, primary_key=True)
    ID_TYPE = Column(String, primary_key=True)

    def get_id(self):
        return uuid5(NAME_SPACE, self.ID_TYPE + self.ID)

    @classmethod
    def from_source(cls, row: MayaStakeholder, **kwargs):
        if row.__class__.__name__ == "MayaStakeholder":
            id_type = ID_TYPE_DICT[row.SugMisparZihui]
            return cls(
                UUID=str(uuid5(NAME_SPACE, id_type + row.MisparZihui)),
                HEBREW_NAME=row.FullName,
                ENGLISH_NAME=row.FullNameEn,
                ID=row.MisparZihui,
                ID_TYPE=id_type,
                **kwargs
            )
        else:
            raise Exception("unknown source: " + row.__class__.__name__)

    @classmethod
    def infer_type(cls, row: MayaStakeholder):
        id_type = ID_TYPE_DICT[row.SugMisparZihui]
        if id_type in ["israeli_id", "passport"]:
            return True
        else:
            return False
