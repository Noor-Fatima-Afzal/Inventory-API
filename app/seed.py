from .extensions import db
from .models import Item

def seed_basic():
    items = [
        Item(sku="SKU-1001", title="Wireless Mouse", description="Ergonomic 2.4GHz mouse", price=12.99, quantity=50),
        Item(sku="SKU-1002", title="Mechanical Keyboard", description="Blue switches", price=54.50, quantity=20),
        Item(sku="SKU-1003", title="USB-C Hub", description="6-in-1 hub", price=24.00, quantity=35),
    ]
    db.session.add_all(items)
    db.session.commit()
