from neomodel import (
    DateTimeFormatProperty,
    FloatProperty,
    IntegerProperty,
    StringProperty,
    StructuredRel,
)


class StakeholderRel(StructuredRel):
    capital_percent = FloatProperty()
    date = DateTimeFormatProperty(format="%Y-%m-%d")
    stock_amount = IntegerProperty()
    notes = StringProperty()
    created_at = DateTimeFormatProperty(format="%Y-%m-%d %H:%M:%S")
    updated_at = DateTimeFormatProperty(default_now=True, format="%Y-%m-%d %H:%M:%S")
