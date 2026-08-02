"""
SAST test fixture - deliberately insecure code patterns.

Every function below demonstrates a well-known vulnerability class so a
static analyzer (SAST) has something to flag. This code is for scanner
validation only. Do not deploy it, import it, or run it against anything
real.
"""

import os
import hashlib
import pickle
import subprocess
import sqlite3
import yaml
import requests
from flask import Flask, request

app = Flask(__name__)

# Hardcoded secret (should be flagged)
SECRET_KEY = "s3cr3t_hardcoded_signing_key_do_not_use"
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/user")
def get_user():
    # SQL injection: unsanitized input concatenated into query
    user_id = request.args.get("id")
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = '" + user_id + "'")
    return str(cur.fetchall())


@app.route("/ping")
def ping():
    # OS command injection: user input passed to a shell
    host = request.args.get("host")
    return subprocess.check_output("ping -c 1 " + host, shell=True)


@app.route("/render")
def render():
    # Path traversal: user-controlled path opened directly
    filename = request.args.get("file")
    with open("/var/www/templates/" + filename) as f:
        return f.read()


@app.route("/fetch")
def fetch():
    # SSRF: user-controlled URL fetched server-side
    url = request.args.get("url")
    return requests.get(url).text


def load_session(blob):
    # Insecure deserialization: pickle on untrusted data -> RCE
    return pickle.loads(blob)


def load_config(raw):
    # Unsafe YAML load: yaml.load without SafeLoader
    return yaml.load(raw)


def hash_password(password):
    # Weak hashing: MD5 for passwords
    return hashlib.md5(password.encode()).hexdigest()


def make_token():
    # Insecure randomness for a security-sensitive value
    import random
    return "".join(random.choice("0123456789abcdef") for _ in range(32))


def run_template(user_code):
    # Code injection: eval on user input
    return eval(user_code)


if __name__ == "__main__":
    # Debug mode enabled + binding to all interfaces
    app.run(host="0.0.0.0", debug=True)
