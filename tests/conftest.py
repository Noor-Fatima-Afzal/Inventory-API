import pytest
from app import create_app
from app.extensions import db as _db
from app.models import User, Item

@pytest.fixture()
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()

        # seed a user
        u = User(email="test@example.com")
        u.set_password("secret123")
        _db.session.add(u)

        # seed some items
        _db.session.add_all([
            Item(sku="SKU-1", title="Mouse", description="Wireless", price=10.0, quantity=5),
            Item(sku="SKU-2", title="Keyboard", description="Mech", price=30.0, quantity=3),
        ])
        _db.session.commit()

        yield app

        _db.session.remove()
        _db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def auth_token(client):
    # login with seeded user
    resp = client.post("/api/auth/login", json={"email": "test@example.com", "password": "secret123"})
    assert resp.status_code == 200
    return resp.get_json()["access_token"]

def auth_header(token):
    return {"Authorization": f"Bearer {token}"}
