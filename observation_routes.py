
from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
import os
import time
#from werkzeug.utils import secure_filename

db_path = "/var/lib/grafana/sqlite_data/dx_agri_project"

observation_bp = Blueprint("observation_bp", __name__)


UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# CRUD untuk Growth Observation
# -----------------------------

# READ
@observation_bp.route("/observations")
def observations():
    try:
        with sqlite3.connect(db_path, timeout=10) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM growth_observation order by case when treatment = 'outdoor-light' then 1 else 2 end, day_of_experiment desc, case when observation_time='afternoon' then 1 when observation_time='noon' then 2 else 3 end")
            rows = cur.fetchall()
        return render_template("observations.html", observations=rows)
    except sqlite3.OperationalError as e:
        print("Database error:", e)
        return f"Database busy or locked: {e}", 500


# CREATE
@observation_bp.route("/add_observation", methods=["POST"])
def add_observation():
    height = request.form.get("height")
    notes = request.form.get("notes")
    day_of_experiment = request.form.get("day_of_experiment")
    observation_time = request.form.get("observation_time")
    treatment = request.form.get("treatment")
    
    photo = request.files.get("photo")
    photo_path = None

    if photo and allowed_file(photo.filename):
        #filename = secure_filename(photo.filename)
        ext = photo.filename.rsplit(".", 1)[1].lower()  # ambil ekstensi file
        timestamp = int(time.time())  # contoh: 1730960123
        filename = f"photo_{timestamp}.{ext}"
        photo.save(os.path.join(UPLOAD_FOLDER, filename))
        photo_path = f"{UPLOAD_FOLDER}/{filename}"

    try:
        with sqlite3.connect(db_path, timeout=10) as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO growth_observation (height, day_of_experiment, observation_time, treatment, notes, photo_path)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (height, day_of_experiment, observation_time, treatment, notes, photo_path))
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Database error:", e)
        return f"Database busy or locked: {e}", 500

    return redirect(url_for("observation_bp.observations"))


# DELETE
@observation_bp.route("/delete_observation/<int:id>", methods=["POST"])
def delete_observation(id):
    try:
        with sqlite3.connect(db_path, timeout=10) as conn:
            cur = conn.cursor()

            # Hapus file foto jika ada
            cur.execute("SELECT photo_path FROM growth_observation WHERE id = ?", (id,))
            row = cur.fetchone()
            if row and row[0] and os.path.exists(row[0]):
                os.remove(row[0])

            cur.execute("DELETE FROM growth_observation WHERE id = ?", (id,))
            conn.commit()
    except sqlite3.OperationalError as e:
        print("Database error:", e)
        return f"Database busy or locked: {e}", 500

    return redirect(url_for("observation_bp.observations"))


# UPDATE (Edit)

@observation_bp.route("/edit_observation/<int:id>", methods=["GET", "POST"])
def edit_observation(id):
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if request.method == "POST":
            height = request.form.get("height")
            notes = request.form.get("notes")
            day_of_experiment = request.form.get("day_of_experiment")
            observation_time = request.form.get("observation_time")
            treatment = request.form.get("treatment")

            photo = request.files.get("photo")
            photo_path = None

            # Ambil foto lama
            cur.execute("SELECT photo_path FROM growth_observation WHERE id = ?", (id,))
            old_photo = cur.fetchone()["photo_path"]

            # Kalau ada foto baru, simpan dan hapus lama
            if photo and allowed_file(photo.filename):
                #filename = secure_filename(photo.filename)
                ext = photo.filename.rsplit(".", 1)[1].lower()  # ambil ekstensi file
                timestamp = int(time.time())
                filename = f"photo_{timestamp}.{ext}"
                photo.save(os.path.join(UPLOAD_FOLDER, filename))
                photo_path = f"{UPLOAD_FOLDER}/{filename}"

                if old_photo and os.path.exists(old_photo):
                    os.remove(old_photo)
            else:
                photo_path = old_photo

            cur.execute("""
                UPDATE growth_observation
                SET height=?, notes=?, day_of_experiment=?, observation_time=?, treatment=?, photo_path=?
                WHERE id=?
            """, (height, notes, day_of_experiment, observation_time, treatment, photo_path, id))
            conn.commit()
            return redirect(url_for("observation_bp.observations"))

        cur.execute("SELECT * FROM growth_observation WHERE id = ?", (id,))
        obs = cur.fetchone()
    return render_template("edit_observation.html", obs=obs)
