from ..models import Item

def total_stock_value(session) -> float:
    """Return the sum of price * quantity across all items."""
    total = 0.0
    for i in session.query(Item).all():
        total += (i.price or 0) * (i.quantity or 0)
    return float(total)
