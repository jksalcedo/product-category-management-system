class Category:
    def __init__(self, id=None, name=None, parent_id=None):
        self.id = id
        self.name = name
        self.parent_id = parent_id

    def to_dict(self):
        return {"id": self.id, "name": self.name, "parent_id": self.parent_id}