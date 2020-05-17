from neomodel import StringProperty
from .business_entity import BusinessEntity


class Person(BusinessEntity):
    name = StringProperty()
