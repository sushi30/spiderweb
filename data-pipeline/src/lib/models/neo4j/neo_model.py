from datetime import datetime
from neomodel import StructuredNode


class NeoModel(StructuredNode):
    @classmethod
    def create_or_update(cls, **kwargs):
        node = cls.nodes.get_or_none(uuid=kwargs["uuid"])
        if node is None:
            node = cls(**kwargs)
        else:
            for k, v in kwargs.items():
                if k != "created_at":
                    setattr(node, k, v)
                node.updated_at = datetime.now()
        node.save()
        return node
