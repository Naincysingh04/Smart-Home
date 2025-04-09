import sqlite3
import time
import random
import requests # type: ignore
from datetime import datetime

# Dummy temperature and humidity function
def read_sensor_data():
    temp = random.uniform(20, 40)
    humidity = random.uniform(30, 60)
    return temp, humidity

# SQLite database
conn = sqlite3.connect("smart_home.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    timestamp TEXT, temperature REAL, humidity REAL)''')
conn.commit()

TEMP_THRESHOLD = 30

while True:
    temp, hum = read_sensor_data()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO sensor_data VALUES (?, ?, ?)", (timestamp, temp, hum))
    conn.commit()
    
    if temp > TEMP_THRESHOLD:
        requests.post("https://api.pushover.net/1/messages.json", data={
            "token": "YOUR_APP_TOKEN",
            "user": "USER_KEY",
            "message": f"Alert! High Temperature: {temp:.2f}°C"
        })
    
    print(f"Logged data: {timestamp}, Temp: {temp:.2f}, Humidity: {hum:.2f}")
    time.sleep(10)