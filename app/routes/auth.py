from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from ..extensions import db
from ..models import User
from ..schemas import RegisterSchema, LoginSchema, UserSchema

auth_bp = Blueprint("auth", __name__)

register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()

@auth_bp.post("/register")
def register():
    data = register_schema.load(request.get_json() or {})
    user = User(email=data["email"], name=data.get("name"))
    user.set_password(data["password"])
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="Email already registered"), 409
    token = create_access_token(identity=user.id)
    return jsonify(user=user_schema.dump(user), access_token=token), 201

@auth_bp.post("/login")
def login():
    data = login_schema.load(request.get_json() or {})
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify(error="Invalid credentials"), 401
    token = create_access_token(identity=user.id)
    return jsonify(access_token=token, user=user_schema.dump(user))

@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user=user_schema.dump(user))
