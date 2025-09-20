import os
import json
from flask import Flask, jsonify, request, send_from_directory, abort

APP_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(APP_DIR, "data")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")
TEMPLATE_FOLDER = os.path.join(APP_DIR, "templates")

os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

app = Flask(__name__, static_folder=TEMPLATE_FOLDER, template_folder=TEMPLATE_FOLDER)

def read_notes():
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def write_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

@app.route("/", methods=["GET"])
def index():
    return send_from_directory(app.template_folder, "index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="UP")

# API: get all notes
@app.route("/api/notes", methods=["GET"])
def api_get_notes():
    return jsonify(read_notes())

# API: get single note
@app.route("/api/notes/<note_id>", methods=["GET"])
def api_get_note(note_id):
    notes = read_notes()
    note = next((n for n in notes if n.get("id") == note_id), None)
    if not note:
        abort(404)
    return jsonify(note)

# API: create a note
@app.route("/api/notes", methods=["POST"])
def api_create_note():
    payload = request.get_json(force=True)
    if not isinstance(payload, dict):
        abort(400)
    notes = read_notes()
    notes.append(payload)
    write_notes(notes)
    return jsonify(payload), 201

# API: update note by id (merge fields)
@app.route("/api/notes/<note_id>", methods=["PUT"])
def api_update_note(note_id):
    payload = request.get_json(force=True)
    notes = read_notes()
    updated = False
    for idx, n in enumerate(notes):
        if n.get("id") == note_id:
            notes[idx] = {**n, **payload}  # merge old and new
            updated = True
            break
    if not updated:
        abort(404)
    write_notes(notes)
    return jsonify(notes[idx])

# API: delete note
@app.route("/api/notes/<note_id>", methods=["DELETE"])
def api_delete_note(note_id):
    notes = read_notes()
    notes2 = [n for n in notes if n.get("id") != note_id]
    write_notes(notes2)
    return jsonify({"deleted": note_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
