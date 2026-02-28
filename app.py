from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    send_file,
    redirect,
    url_for
)
from pathlib import Path
from werkzeug.utils import secure_filename
import string
import random

app = Flask(__name__)

# ----------------------------
# Configuration
# ----------------------------
UPLOAD_FOLDER = Path("Storage")
UPLOAD_FOLDER.mkdir(exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB limit


# ----------------------------
# Helpers
# ----------------------------
def token_gen(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

database = []

def load_database():
    """
    Dynamically build file database.
    This avoids crashing at startup.
    """

    for file in UPLOAD_FOLDER.iterdir():
        if file.is_file():
            database.append({
                "path": str(file),
                "filename": file.name,
                "suffix": file.suffix,
                "token": token_gen()
            })

    return database

def filedelete(token):
    for item in database:
        if token in item["token"]:
            Path(item["path"]).unlink()
            database.remove(item)
            return 200
    return 404
# ----------------------------
# Routes
# ----------------------------

@app.route("/")
def index():
    return render_template("index.html", app="Nora")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return jsonify({"message": "No file provided"}), 400

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    filename = secure_filename(file.filename)
    save_path = UPLOAD_FOLDER / filename

    file.save(save_path)

    return jsonify({"message": "File uploaded successfully"}), 200

@app.route("/songs")
def songs():
    if not database:
        return redirect(url_for('scan'))
    return jsonify(database)


@app.route("/songs/<token>")
def file_access(token):

    for item in database:
        if item["token"] == token:
            return send_file(
                item["path"],
                as_attachment=False,
                download_name=item["filename"]
            )

    return jsonify({"message": "File not found"}), 404


@app.route("/test")
def test():
    return "App is working!"
@app.route("/clear/<token>")
def clear(token):
    result = filedelete(token)
    if result == 200:
        return redirect(url_for('scan'))
    return jsonify({"message": "Failed to delete file"}), 404

@app.route("/scan")
def scan():
    load_database()
    if not database:
        return redirect(url_for('index'))
    return redirect(url_for('songs'))
# ----------------------------
# Entry
# ----------------------------
