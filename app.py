from flask import Flask, jsonify, render_template, request, redirect, url_for
import threading
import time
import sqlite3
from datetime import datetime
import board, busio, adafruit_sht31d
from datetime import datetime, timezone, timedelta
from observation_routes import observation_bp

# Misal untuk JST (UTC+9)
def current_jst_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


app = Flask(__name__)

# -----------------------------
# Sensor initialization
# -----------------------------
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c, address=0x44)

# -----------------------------
# SQLite DB
# -----------------------------
db_path = "/var/lib/grafana/sqlite_data/dx_agri_project"
conn = sqlite3.connect(db_path, check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_mbeans_logging (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp_ DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature REAL,
    humidity REAL,
    day_of_experiment INTEGER,
    observation_time TEXT,
    treatment TEXT
)
""")
conn.commit()

# -----------------------------
# Sensor reading function
# -----------------------------
def read_sensor():
    try:
        temp = round(sensor.temperature, 2)
        hum = round(sensor.relative_humidity, 2)
        return {"temp": temp, "hum": hum}
    except Exception as e:
        print("Sensor read error:", e)
        time.sleep(1)  # beri waktu 1 detik sebelum lanjut
        return {"temp": None, "hum": None}

# -----------------------------
# Logging thread
# -----------------------------
logging_thread = None
logging_status = {"running": False, "start_time": None, "duration_sec": 0}  # 15 menit

def log_sensor(day, obs_time, treatment,rec_duration):
    global stop_logging, logging_status
    stop_logging = False
    logging_status["running"] = True
    logging_status["start_time"] = datetime.now(timezone(timedelta(hours=9)))
    logging_status["duration_sec"] = float(rec_duration)  # simpan durasi di sini

    start_time = time.time()

    while not stop_logging and (time.time() - start_time < logging_status["duration_sec"]):
        data = read_sensor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO sensor_mbeans_logging (timestamp_, temperature, humidity, day_of_experiment, observation_time, treatment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, data["temp"], data["hum"], day, obs_time, treatment))
        conn.commit()
        time.sleep(2)

    stop_logging = True
    logging_status["running"] = False


# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global logging_thread
    day = int(request.form.get('day_of_experiment'))
    obs_time = request.form.get('observation_time')
    treatment = request.form.get('treatment')
    rec_duration= request.form.get('recording_duration')
    
    if logging_thread is None or not logging_thread.is_alive():
        logging_thread = threading.Thread(target=log_sensor, args=(day, obs_time, treatment, rec_duration))
        logging_thread.start()
    
    return jsonify({"status": "started"})
    
@app.route('/status')
def status():
    
    if logging_status["running"]:
        elapsed = (datetime.now(timezone(timedelta(hours=9))) - logging_status["start_time"]).total_seconds()
        remaining = max(0, logging_status["duration_sec"] - elapsed)
    else:
        remaining = 0
    return jsonify({
        "running": logging_status["running"],
        "remaining_sec": int(remaining)
    })


@app.route('/data')
def data():
    sensor_data = read_sensor()
    return jsonify(sensor_data)
    
    
# register blueprint
app.register_blueprint(observation_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
