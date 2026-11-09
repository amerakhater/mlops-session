def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_crud_flow(client):
    created = client.post(
        "/items", json={"name": "  Laptop ", "description": "16GB", "price": 999.99}
    )
    assert created.status_code == 201
    item = created.json()
    assert item["name"] == "Laptop"  # whitespace stripped
    item_id = item["id"]

    assert client.get(f"/items/{item_id}").json()["price"] == "999.99"
    assert len(client.get("/items").json()) == 1

    updated = client.patch(f"/items/{item_id}", json={"price": 899.5})
    assert updated.status_code == 200
    assert updated.json()["price"] == "899.50"
    assert updated.json()["description"] == "16GB"  # untouched by partial update

    assert client.delete(f"/items/{item_id}").status_code == 204
    assert client.get(f"/items/{item_id}").status_code == 404


def test_create_validation_errors(client):
    resp = client.post("/items", json={"name": "", "price": -1, "unknown": 1})
    assert resp.status_code == 422
    error_types = {e["type"] for e in resp.json()["detail"]}
    assert {"string_too_short", "greater_than_equal", "extra_forbidden"} <= error_types


def test_missing_item_returns_404(client):
    assert client.get("/items/999").status_code == 404
    assert client.patch("/items/999", json={"name": "x"}).status_code == 404
    assert client.delete("/items/999").status_code == 404


def test_list_pagination_limits(client):
    assert client.get("/items?limit=0").status_code == 422
    assert client.get("/items?skip=-1").status_code == 422
