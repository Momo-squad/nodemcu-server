from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from datetime import datetime
import sqlite3
import threading

_db_local = threading.local()
app = FastAPI()
conn = sqlite3.connect('data.db')
relay_state = "off"

def get_connection():
    if hasattr(_db_local, "connection"):
        return _db_local.connection
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    _db_local.connection = conn
    _db_local.cursor = cursor
    return conn

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/maris")
async def maris():
    return {"message": "chaina."}


@app.get("/relay-state")
async def relay_s():
    return relay_state

@app.get("/relay/{state}")
async def relay(state: str):
    global relay_state
    relay_state = state
    return {"message": f"changed state to {state}."}

@app.get("/data")
def get_all_data():
    c = get_connection().cursor()
    c.execute("SELECT * FROM sensor_data")
    data = c.fetchall()
    return {"data": data}

@app.get("/sensor-data/{temp}/{hum}/{mois}/{lig}")
def store_sensor_data(temp, hum, mois, lig):
    print(temp, hum, mois, lig)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = get_connection().cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data (timestamp TEXT, temperature REAL, humidity REAL, moisture REAL, light REAL)''')
    c.execute("INSERT INTO sensor_data (timestamp, temperature, humidity, moisture, light) VALUES (?, ?, ?, ?, ?)", 
              (timestamp, temp, hum, mois, lig)
        )
    conn.commit()
    return {"message": "Sensor data stored successfully."}


