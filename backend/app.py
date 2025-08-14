from flask import Flask, request, jsonify
from flask_cors import CORS
import os, requests
from db import init_db, get_conn
from image_utils import overlay_tattoo

A1111_BASE = os.getenv("A1111_BASE", "http://127.0.0.1:7860")
STATIC_FOLDER = "static"

app = Flask(__name__)
CORS(app)
init_db()

os.makedirs(f"{STATIC_FOLDER}/images", exist_ok=True)
os.makedirs(f"{STATIC_FOLDER}/overlays", exist_ok=True)

@app.route("/api/login", methods=["POST"])
def login():
    username = request.json.get("username")
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (username,))
    conn.commit()
    c.execute("SELECT id FROM users WHERE username=?", (username,))
    user_id = c.fetchone()[0]
    conn.close()
    return jsonify({"token": str(user_id)})

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data["prompt"]
    user_id = int(data["user_id"])

    payload = {
        "prompt": prompt,
        "steps": data.get("steps", 20),
        "width": data.get("width", 512),
        "height": data.get("height", 512)
    }
    res = requests.post(f"{A1111_BASE}/sdapi/v1/txt2img", json=payload).json()
    import base64
    img_data = base64.b64decode(res["images"][0])
    img_path = f"{STATIC_FOLDER}/images/tattoo_{user_id}_{len(os.listdir(f'{STATIC_FOLDER}/images'))}.png"
    with open(img_path, "wb") as f:
        f.write(img_data)

    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO images (user_id, url, prompt) VALUES (?, ?, ?)",
              (user_id, img_path, prompt))
    conn.commit()
    conn.close()

    return jsonify({"url": img_path})

@app.route("/api/images")
def images():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT url, prompt FROM images ORDER BY id DESC LIMIT 20")
    data = [{"url": row[0], "prompt": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(data)

@app.route("/api/my-images")
def my_images():
    user_id = request.args.get("user_id")
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT url, prompt FROM images WHERE user_id=? ORDER BY id DESC", (user_id,))
    data = [{"url": row[0], "prompt": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(data)

@app.route("/api/overlay", methods=["POST"])
def overlay():
    base_file = request.files["base"]
    tattoo_file = request.files["tattoo"]

    base_path = f"{STATIC_FOLDER}/overlays/{base_file.filename}"
    tattoo_path = f"{STATIC_FOLDER}/overlays/{tattoo_file.filename}"
    base_file.save(base_path)
    tattoo_file.save(tattoo_path)

    x = int(request.form.get("x"))
    y = int(request.form.get("y"))
    scale = float(request.form.get("scale"))
    rotation = float(request.form.get("rotation"))
    opacity = float(request.form.get("opacity"))

    out_path = overlay_tattoo(base_path, tattoo_path, x, y, scale, rotation, opacity)
    return jsonify({"url": out_path})

if __name__ == "__main__":
    app.run(debug=True)
