"""Inventory service for the DevSecOps lab (Assignment 9).

Fixed version: every Flake8/bandit and CodeQL finding from the first
version has been fixed or, where it is a false positive, explicitly
suppressed with a reason.
"""
import ipaddress
import os
import sqlite3
import subprocess  # noqa: S404 - needed for ping; input is validated below

from flask import Flask, abort, jsonify, request

app = Flask(__name__)

# Secrets come from the environment (e.g. a GitHub secret), never from source code.
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")


def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE stock (sku TEXT, qty INTEGER)")
    conn.execute("INSERT INTO stock VALUES ('TICKET-01', 42)")
    return conn


@app.route("/inventory")
def inventory():
    sku = request.args.get("sku", "TICKET-01")
    conn = get_db()
    # Parameterized query: the driver escapes the value -> no SQL injection
    row = conn.execute("SELECT qty FROM stock WHERE sku = ?", (sku,)).fetchone()
    return jsonify(sku=sku, qty=row[0] if row else 0)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # Allow only a valid IP address, then pass a fixed argument list (no shell)
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        abort(400, "host must be an IP address")
    result = subprocess.run(  # noqa: S603 - fixed argv, no shell, validated IP
        ["/usr/bin/ping", "-c", "1", str(ip)],
        capture_output=True,
        text=True,
        timeout=5,
    )
    return jsonify(output=result.stdout)


if __name__ == "__main__":
    # Local only, debug off unless explicitly enabled
    app.run(host="127.0.0.1", port=8081, debug=os.environ.get("FLASK_DEBUG") == "1")
