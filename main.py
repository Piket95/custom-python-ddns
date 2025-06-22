from flask import Flask, request, render_template
from datetime import datetime

import json
import os
import subprocess

app = Flask(__name__)

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('404.html'), 404

@app.route('/update')
def update():
    user = request.args.get('user', '')
    password = request.args.get('password', '')
    host = request.args.get('host', '')
    ip = request.args.get('ip', '')

    # Prüfen, ob User existiert und Passwort-Hash stimmt
    check_result = check_user(user, password)
    if check_result:
        # Host und IP aktualisieren
        if update_user_data(user, password, host, ip):
            remove_dns_record_from_bind(host, ip)
            log = add_dns_record_to_bind(host, ip)
            return f"Zugriff erlaubt, Daten aktualisiert <br> {log}", 200
        else:
            return "Interner Fehler", 500
    elif check_result is None:
        # User existiert nicht -> anlegen
        if add_user(user, password, host, ip):
            add_dns_record_to_bind(host, ip)
            return "Neuer User angelegt", 201
        else:
            return "Interner Fehler", 500
    else:
        return "Zugriff verweigert", 403


def read_users():
    if not os.path.exists('data/users.json'):
        return {"users": []}
    with open('data/users.json', 'r') as f:
        return json.load(f)

def write_users(data):
    with open('data/users.json', 'w') as f:
        json.dump(data, f, indent=4)

def check_user(user, password):
    users = read_users()
    for u in users['users']:
        if u['user'] == user:
            return u['password'] == password  # True, wenn Passwort-Hash stimmt
    return None  # User existiert nicht

def add_user(user, password, host, ip):
    users = read_users()
    for u in users['users']:
        if u['user'] == user:
            return False  # User existiert bereits
    users['users'].append({
        "user": user,
        "password": password,
        "host": host,
        "ip": ip
    })
    write_users(users)
    return True

def update_user_data(user, password, host, ip):
    users = read_users()
    for u in users['users']:
        if u['user'] == user and u['password'] == password:
            # Passwort stimmt, also host und ip aktualisieren
            u['host'] = host
            u['ip'] = ip
            write_users(users)
            return True
    return False

def add_dns_record_to_bind(host, ip):
    nsupdate_cmds = f"""
    server 127.0.0.1
    zone {os.environ["ZONE"]}
    update add {host}. 3600 A {ip}
    send
    """

    with open("test.txt", "w") as f:
        f.write(nsupdate_cmds)

    return execute_bind_command(nsupdate_cmds)


def remove_dns_record_from_bind(host, ip):
    nsupdate_cmds = f"""
    server 127.0.0.1
    zone {os.environ["ZONE"]}
    update delete {host}. A
    send
    """

    return execute_bind_command(nsupdate_cmds)

def execute_bind_command(command):
    # Log-Datei
    log_dir = "./data/"
    log_file = os.path.join(log_dir, "bind_updates.log")

    # Verzeichnis erstellen, falls nicht vorhanden
    os.makedirs(log_dir, exist_ok=True)

    # Kommando ausführen
    result = subprocess.run(
        ['nsupdate'],
        input=command.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Ausgabe und Fehler dekodieren
    output = result.stdout.decode()
    errors = result.stderr.decode()

    # Log-Eintrag erstellen
    log_entry = (
        f"Timestamp: {datetime.now().isoformat()}\n"
        f"Exit code: {result.returncode}\n"
        f"Command: {command}\n"
        f"Output: {output}\n"
        f"Errors: {errors}\n"
        "------------------------------------\n"
    )

    # Log-Eintrag ans Dateiende schreiben (append)
    # with open(log_file, "a", encoding="utf-8") as f:
    #     f.write(log_entry)

    return log_entry

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
