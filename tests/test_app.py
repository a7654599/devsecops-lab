import subprocess

import app as app_module


def client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_inventory_returns_stock():
    resp = client().get("/inventory?sku=TICKET-01")
    assert resp.status_code == 200
    assert resp.get_json()["qty"] == 42


def test_inventory_unknown_sku():
    resp = client().get("/inventory?sku=NOPE")
    assert resp.get_json()["qty"] == 0


def test_ping_ok(monkeypatch):
    # do not run a real ping in CI
    monkeypatch.setattr(
        app_module.subprocess,
        "run",
        lambda *a, **k: subprocess.CompletedProcess(a, 0, stdout="1 packets received", stderr=""),
    )
    resp = client().get("/ping?host=127.0.0.1")
    assert resp.status_code == 200
    assert "received" in resp.get_json()["output"]


def test_ping_rejects_injection():
    # the old version would have run "ping -c 1 127.0.0.1; cat /etc/passwd"
    resp = client().get("/ping?host=127.0.0.1;cat%20/etc/passwd")
    assert resp.status_code == 400


def test_inventory_sql_injection_is_harmless():
    # the old version returned stock for "' OR '1'='1"
    resp = client().get("/inventory?sku=' OR '1'='1")
    assert resp.get_json()["qty"] == 0
