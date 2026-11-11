"""Inventory service for the DevSecOps lab (Assignment 9).

This first version deliberately contains common security and quality
problems so that the linter (Flake8 + flake8-bandit) and the SAST tool
(CodeQL) have something to find. The password below is a FAKE demo value.
"""
import json
import os
import sqlite3
import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)

DB_PASSWORD = "SuperSecret123"  # fake demo value: hardcoded password


def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE stock (sku TEXT, qty INTEGER)")
    conn.execute("INSERT INTO stock VALUES ('TICKET-01', 42)")
    return conn


@app.route("/inventory")
def inventory():
    sku = request.args.get("sku", "TICKET-01")
    conn = get_db()
    # SQL built with string formatting -> SQL injection
    row = conn.execute("SELECT qty FROM stock WHERE sku = '%s'" % sku).fetchone()
    return jsonify(sku=sku, qty=row[0] if row else 0)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # user input passed to a shell -> command injection
    result = subprocess.run("ping -c 1 " + host, shell=True, capture_output=True, text=True)
    return jsonify(output=result.stdout)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, debug=True)
