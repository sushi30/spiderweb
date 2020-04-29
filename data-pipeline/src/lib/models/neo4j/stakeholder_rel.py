from neomodel import FloatProperty, StructuredRel, DateProperty, IntegerProperty, StringProperty


class StakeholderRel(StructuredRel):
    capital_percent = FloatProperty()
    date = DateProperty()
    stock_amount = IntegerProperty()
    notes = StringProperty()
