from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import or_
from ..extensions import db
from ..models import Item
from ..schemas import ItemSchema

items_bp = Blueprint("items", __name__)
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@items_bp.get("/")
@jwt_required(optional=True)  # allow anonymous reads
def list_items():
    q = request.args.get("q", "").strip()
    page = max(int(request.args.get("page", 1)), 1)
    per_page = min(max(int(request.args.get("per_page", 10)), 1), 100)

    query = Item.query
    if q:
        ilike = f"%{q}%"
        query = query.filter(
            or_(Item.sku.ilike(ilike), Item.title.ilike(ilike), Item.description.ilike(ilike))
        )
    pagination = query.order_by(Item.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify(
        items=items_schema.dump(pagination.items),
        meta={"page": page, "per_page": per_page, "total": pagination.total}
    )

@items_bp.post("/")
@jwt_required()
def create_item():
    payload = item_schema.load(request.get_json() or {})
    item = Item(**payload)
    db.session.add(item)
    db.session.commit()
    return jsonify(item=item_schema.dump(item)), 201

@items_bp.get("/<int:item_id>")
@jwt_required(optional=True)
def get_item(item_id: int):
    item = Item.query.get_or_404(item_id)
    return jsonify(item=item_schema.dump(item))

@items_bp.put("/<int:item_id>")
@jwt_required()
def update_item(item_id: int):
    item = Item.query.get_or_404(item_id)
    payload = item_schema.load(request.get_json() or {}, partial=True)
    for k, v in payload.items():
        setattr(item, k, v)
    db.session.commit()
    return jsonify(item=item_schema.dump(item))

@items_bp.delete("/<int:item_id>")
@jwt_required()
def delete_item(item_id: int):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(status="deleted")
