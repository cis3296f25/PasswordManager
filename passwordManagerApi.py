import sqlite3
from flask import Flask, jsonify, Blueprint, request
from cryptography.fernet import Fernet
import secrets
import os

KEY_FILE = "vault.key"

# Database setup (should eventually be refactored to repository layer) ###############
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

cipher = Fernet(key)

conn = sqlite3.connect("vault.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS credentials (
    site TEXT,
    username TEXT,
    password BLOB
)
""")
conn.commit()
########################################################################################

# Flask API
app = Flask(__name__)
ROUTE = "/credentials"

# POST Methods ##################################################################################
@app.route(ROUTE, methods=["POST"])
def add_credential():
    data = request.json
    encrypted_password = cipher.encrypt(data["password"].encode())
    c.execute(
        "INSERT INTO credentials (site, username, password) VALUES (?, ?, ?)",
        (data["site"], data["username"], encrypted_password)
    )
    conn.commit()
    return jsonify({"status": "added"})

# GET Methods ###################################################################################
@app.route(ROUTE + "/<site>", methods=["GET"])
def get_credential(site):
    c.execute("SELECT username, password FROM credentials WHERE site = ?", (site,))
    row = c.fetchone()
    if row:
        username, encrypted_password = row
        password = cipher.decrypt(encrypted_password).decode()
        return jsonify({"site": site, "username": username, "password": password})
    return jsonify({"error": "not found"})

# Password generator
@app.route(ROUTE + "/generate-password", methods=["GET"])
def generate_password(length=12):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return jsonify({"generatedPassword": password})

# DELETE Methods ###################################################################################
@app.route(ROUTE + "/<site>", methods=["DELETE"])
def delete_credential(site):
    c.execute("DELETE FROM credentials WHERE site = ?", (site,))
    conn.commit()
    return jsonify({"status": "deleted"})

# Password generator
def generate_password(length=12):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return ''.join(secrets.choice(chars) for _ in range(length))

# Test and run
if __name__ == "__main__":
    # Run server
    app.run(port=5000)