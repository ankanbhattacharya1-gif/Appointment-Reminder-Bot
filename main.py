import re
from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
import sqlite3

app = FastAPI(title="Appointment Reminder Chatbot")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("appointments.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_name TEXT,
    contact TEXT,
    channel TEXT,
    appointment_time TEXT,
    preferences TEXT
)
""")
conn.commit()

# ---------------- DATA MODEL ----------------
class Appointment(BaseModel):
    patient_name: str
    contact: str
    channel: str
    appointment_time: datetime
    preferences: str
class ChatMessage(BaseModel):
    patient_name: str
    contact: str
    message: str


# ---------------- DATA COMPRESSION ----------------
def compress_appointment(appt: Appointment):
    return f"{appt.patient_name}|{appt.channel}|{appt.appointment_time.isoformat()}|{appt.preferences}"

# ---------------- REMINDER ENGINE ----------------
def send_reminder(row):
    name, contact, channel, time, prefs = row
    print(f"[REMINDER] {name} → {contact} via {channel} at {time}")
def parse_message(message: str):
    message = message.lower()

    # communication channel
    if "email" in message:
        channel = "email"
    elif "sms" in message or "text" in message:
        channel = "sms"
    else:
        channel = "email"

    # date
    if "tomorrow" in message:
        appt_date = date.today() + timedelta(days=1)
    else:
        appt_date = date.today()

    # time
    match = re.search(r"(\\d{1,2})(:?\\d{2})?\\s?(am|pm)?", message)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)[1:]) if match.group(2) else 0
        ampm = match.group(3)
        if ampm == "pm" and hour < 12:
            hour += 12
    else:
        hour, minute = 9, 0  # default time

    return datetime(
        appt_date.year,
        appt_date.month,
        appt_date.day,
        hour,
        minute
    ), channel


# ---------------- API ENDPOINTS ----------------
@app.post("/schedule")
def schedule_appointment(appt: Appointment):
    cursor.execute(
        "INSERT INTO appointments (patient_name, contact, channel, appointment_time, preferences) VALUES (?,?,?,?,?)",
        (
            appt.patient_name,
            appt.contact,
            appt.channel,
            appt.appointment_time.isoformat(),
            appt.preferences
        )
    )
    conn.commit()

    return {
        "status": "scheduled",
        "compressed_data": compress_appointment(appt)
    }

@app.get("/check_reminders")
def check_reminders():
    now = datetime.utcnow()
    upcoming = now + timedelta(hours=24)

    cursor.execute(
        "SELECT patient_name, contact, channel, appointment_time, preferences FROM appointments"
    )
    rows = cursor.fetchall()

    sent = []
    for r in rows:
        appt_time = datetime.fromisoformat(r[3])
        if now < appt_time <= upcoming:
            send_reminder(r)
            sent.append(r[0])

    return {"reminders_sent": sent}
@app.post("/chat")
def chat(msg: ChatMessage):
    appointment_time, channel = parse_message(msg.message)

    cursor.execute(
        "INSERT INTO appointments (patient_name, contact, channel, appointment_time, preferences) VALUES (?,?,?,?,?)",
        (
            msg.patient_name,
            msg.contact,
            channel,
            appointment_time.isoformat(),
            msg.message
        )
    )
    conn.commit()

    compressed = f"{msg.patient_name}|{channel}|{appointment_time.isoformat()}|{msg.message}"

    return {
        "bot": "✅ Appointment booked from chat",
        "compressed_data": compressed
    }
