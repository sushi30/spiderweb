from uuid import UUID, uuid5
from sqlalchemy import Column, String
from .. import Base, WithTimestamps, WithUUID
from ..constants import ID_TYPE_DICT
from ..db_model import DbModel
from ..maya_stakeholders import MayaStakeholder

NAME_SPACE = UUID("0468c360-3ab5-46a1-ae34-466b6b7b808c")


class Firm(WithTimestamps, WithUUID, DbModel, Base):
    __tablename__ = "firm"

    HEBREW_NAME = Column(String)
    ENGLISH_NAME = Column(String)
    ID = Column(String, primary_key=True)
    ID_TYPE = Column(String, primary_key=True)

    def get_id(self):
        return uuid5(NAME_SPACE, self.ID_TYPE + self.ID)

    @classmethod
    def from_source(cls, source: type, row: MayaStakeholder, **kwargs):
        if source.__name__ == "MayaStakeholder":
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
            raise Exception("unknown source: " + source.__name__)

    @classmethod
    def infer_type(cls, row: MayaStakeholder):
        id_type = ID_TYPE_DICT[row.SugMisparZihui]
        if id_type in [
            "israeli_company_registrar",
            "israeli_company_registrar_foreign_company",
            "israeli_group_registrar",
        ]:
            return True
        else:
            return False
