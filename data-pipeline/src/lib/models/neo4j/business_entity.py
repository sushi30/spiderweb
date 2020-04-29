from neomodel import StructuredNode, StringProperty, RelationshipTo
from models.neo4j import Firm
from models.neo4j.stakeholder_rel import StakeholderRel


class BusinessEntity(StructuredNode):
    id = StringProperty(unique_index=True)

    stakeholder = RelationshipTo(Firm, "STAKEHOLDER", model=StakeholderRel)
