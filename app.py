from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import time
import uuid

app = Flask(__name__)

# Where to store uploaded files
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# In-memory store: id -> {type, value, created_at, filename(optional)}
clips = {}
TTL_SECONDS = 24 * 60 * 60  # 24 hours


def cleanup():
    """Remove expired clips from memory and delete their files."""
    now = time.time()
    expired_ids = []
    for cid, data in list(clips.items()):
        if now - data["created_at"] > TTL_SECONDS:
            expired_ids.append(cid)

    for cid in expired_ids:
        info = clips.pop(cid, None)
        if info and info["type"] in ("image", "file"):
            # Delete file from disk if it exists
            fname = info.get("filename")
            if fname:
                path = os.path.join(UPLOAD_FOLDER, fname)
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass


def generate_id():
    # 6-character ID with letters/numbers, easy to read
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(chars[uuid.uuid4().int % len(chars)] for _ in range(6))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/clipboard", methods=["POST"])
def create_clip():
    cleanup()
    clip_type = request.form.get("type")

    if clip_type == "text":
        text = request.form.get("text", "").strip()
        if not text:
            return jsonify({"error": "Text is empty"}), 400

        cid = generate_id()
        clips[cid] = {
            "type": "text",
            "value": text,
            "created_at": time.time(),
        }
        return jsonify({"id": cid, "type": "text"})

    elif clip_type in ("image", "file"):
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        filename = secure_filename(file.filename)
        if not filename:
            return jsonify({"error": "Invalid filename"}), 400

        # Optional: enforce simple size/type rules here

        cid = generate_id()
        # Prefix with ID to avoid collisions
        stored_name = f"{cid}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, stored_name)
        file.save(file_path)  # basic Flask upload pattern [web:20][web:23][web:26]

        clips[cid] = {
            "type": clip_type,
            "value": stored_name,
            "created_at": time.time(),
            "filename": stored_name,
            "original_name": filename,
        }
        return jsonify({"id": cid, "type": clip_type, "filename": filename})

    else:
        return jsonify({"error": "Unsupported type"}), 400


@app.route("/api/clipboard/<cid>", methods=["GET"])
def get_clip(cid):
    cleanup()
    data = clips.get(cid)
    if not data:
        return jsonify({"error": "Not found or expired"}), 404

    # For text, return JSON; for image/file, return JSON with download URL
    if data["type"] == "text":
        return jsonify({
            "id": cid,
            "type": "text",
            "text": data["value"],
        })
    else:
        return jsonify({
            "id": cid,
            "type": data["type"],
            "filename": data.get("original_name", data.get("filename")),
            "download_url": f"/download/{cid}",
        })


@app.route("/download/<cid>")
def download_clip(cid):
    cleanup()
    data = clips.get(cid)
    if not data or data["type"] not in ("image", "file"):
        return "Not found or not a file", 404

    stored_name = data.get("filename")
    if not stored_name:
        return "File missing", 404

    # send_from_directory will serve the file from /uploads [web:20][web:22][web:23]
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        stored_name,
        as_attachment=True,
        download_name=data.get("original_name", stored_name),
    )


if __name__ == "__main__":
    app.run(debug=True)
