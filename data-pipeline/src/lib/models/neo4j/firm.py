from neomodel import StringProperty
from .business_entity import BusinessEntity


class Firm(BusinessEntity):
    name = StringProperty()
