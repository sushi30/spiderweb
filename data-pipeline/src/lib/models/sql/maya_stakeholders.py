from datetime import datetime

from utils.dictionary import rename
from . import Base, WithTimestamps, DbModel
from sqlalchemy import Column, DateTime, Date, String, Integer, Float, Text


class MayaStakeholder(WithTimestamps, DbModel, Base):
    __tablename__ = "maya_stakeholder"

    created_at = Column(DateTime, nullable=False, primary_key=True)
    AccumulateHoldings = Column(String, default=None)
    AsmachtaDuachMeshubash = Column(String, default=None)
    IsRequiredToReportChange = Column(String, default=None)
    KodSugYeshut = Column(String, default=None)
    HolderOwner = Column(String, default=None)
    CapitalPct = Column(Float, default=None)
    CapitalPct_Dilul = Column(Float, default=None)
    ChangeSincePrevious = Column(Integer, default=None)
    CompanyName = Column(String, default=None)
    CompanyNameEn = Column(String, default=None)
    CompanyUrl = Column(String, default=None)
    CurrentAmount = Column(Integer, default=None)
    Date2 = Column(Date, default=None)
    FullName = Column(String, default=None)
    FullNameEn = Column(String, default=None)
    HeaderMisparBaRasham = Column(String, default=None)
    HeaderSemelBursa = Column(String, default=None)
    IsFrontForOthers = Column(String, default=None)
    MaximumRetentionRate = Column(String, default=None)
    MezahehHotem = Column(Integer, default=None)
    MezahehTofes = Column(Integer, default=None)
    MezahehYeshut = Column(String, default=None)
    MinimumRetentionRate = Column(String, default=None)
    MisparNiarErech = Column(Integer, default=None)
    MisparZihui = Column(String, primary_key=True)
    Nationality = Column(String, default=None)
    NeyarotErechReshumim = Column(String, default=None)
    Notes = Column(Text, default=None)
    Position = Column(String, default=None)
    PreviousAmount = Column(Integer, default=None)
    PreviousCompanyNames = Column(String, default=None)
    PumbiLoPumbi = Column(String, default=None)
    StockName = Column(String, primary_key=True)
    SugMisparZihui = Column(String, primary_key=True, default=None)
    TreasuryShares = Column(String, default=None)
    VotePower = Column(Float, default=None)
    VotePower_Dilul = Column(Float, default=None)
    company = Column(String, default=None)
    date = Column(DateTime, default=None)
    fix_for = Column(String, default=None)
    fixed_by = Column(String, default=None)
    id = Column(String, default=None)
    next_doc = Column(String, default=None)
    prev_doc = Column(String, default=None)
    stakeholder_type = Column(String, default=None)
    type = Column(String, default=None)
    url = Column(String, default=None)

    @classmethod
    def from_dict(cls, dictionary, **kwargs):
        dictionary = rename(dictionary, "Date", "Date2")
        dictionary["date"] = datetime.fromisoformat(dictionary["date"])
        dictionary["Date2"] = datetime.strptime(dictionary["Date2"], "%d/%m/%Y")
        return cls(**dictionary, **kwargs)
