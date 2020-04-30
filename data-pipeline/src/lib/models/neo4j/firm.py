from neomodel import StringProperty, RelationshipFrom
from . import StakeholderRel
from .business_entity import BusinessEntity


class Firm(BusinessEntity):
    name = StringProperty()

    stakeholder = RelationshipFrom(BusinessEntity, "STAKEHOLDER", model=StakeholderRel)
