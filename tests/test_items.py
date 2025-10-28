from .conftest import auth_header

def test_list_items_public(client):
    r = client.get("/api/items/")
    assert r.status_code == 200
    data = r.get_json()
    assert "items" in data and len(data["items"]) >= 2

def test_create_item_requires_auth(client):
    r = client.post("/api/items/", json={
        "sku": "SKU-NEW",
        "title": "USB Hub",
        "description": "7 ports",
        "price": 20.5,
        "quantity": 10
    })
    assert r.status_code in (401, 422, 400)

def test_create_update_delete_item(client, auth_token):
    create = client.post("/api/items/", json={
        "sku": "SKU-NEW",
        "title": "USB Hub",
        "description": "7 ports",
        "price": 20.5,
        "quantity": 10
    }, headers=auth_header(auth_token))
    assert create.status_code == 201
    item_id = create.get_json()["item"]["id"]

    # update
    upd = client.put(f"/api/items/{item_id}", json={"price": 21.0}, headers=auth_header(auth_token))
    assert upd.status_code == 200
    assert upd.get_json()["item"]["price"] == 21.0

    # fetch
    got = client.get(f"/api/items/{item_id}")
    assert got.status_code == 200
    assert got.get_json()["item"]["sku"] == "SKU-NEW"

    # delete
    dele = client.delete(f"/api/items/{item_id}", headers=auth_header(auth_token))
    assert dele.status_code == 200

    # ensure gone
    notfound = client.get(f"/api/items/{item_id}")
    assert notfound.status_code == 404
