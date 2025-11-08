class Product:
    def __init__(self, id=None, name=None, price=None, category_id=None):
        self.id = id
        self.name = name
        self.price = price
        self.category_id = category_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category_id": self.category_id,
        }