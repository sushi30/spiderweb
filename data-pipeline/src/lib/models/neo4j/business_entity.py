from neomodel import StructuredNode, StringProperty


class BusinessEntity(StructuredNode):
    id = StringProperty(unique_index=True)
