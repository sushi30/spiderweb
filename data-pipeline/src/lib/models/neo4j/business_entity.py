from neomodel import DateTimeFormatProperty, StringProperty
from .neo_model import NeoModel


class BusinessEntity(NeoModel):
    uuid = StringProperty(unique_index=True)
    created_at = DateTimeFormatProperty(format="%Y-%m-%d %H:%M:%S")
    updated_at = DateTimeFormatProperty(default_now=True, format="%Y-%m-%d %H:%M:%S")
