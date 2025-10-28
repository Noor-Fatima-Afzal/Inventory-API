def test_register_and_login_flow(client):
    r = client.post("/api/auth/register", json={
        "email": "new@example.com",
        "password": "mypass123",
        "name": "Newbie"
    })
    assert r.status_code == 201
    token = r.get_json()["access_token"]
    assert token

    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.get_json()["user"]["email"] == "new@example.com"

def test_login_invalid(client):
    r = client.post("/api/auth/login", json={"email": "nope@x.com", "password": "zzz"})
    assert r.status_code == 401
