from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Configuration de la base de données
DB_CONFIG = {
    "dbname": "ceetiz_db",
    "user": "postgres",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

class Activity(BaseModel):
    title: str
    price: str
    location: str
    image: str
    url: str

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

@app.post("/activities/")
async def create_activity(activity: Activity):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO activities (title, price, location, image, url) VALUES (%s, %s, %s, %s, %s)"
    values = (activity.title, activity.price, activity.location, activity.image, activity.url)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Activity created successfully"}

@app.get("/activities/")
async def get_activities():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM activities")
    activities = cursor.fetchall()
    cursor.close()
    conn.close()
    return activities

@app.get("/activities/{activity_id}")
async def get_activity(activity_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM activities WHERE id = %s", (activity_id,))
    activity = cursor.fetchone()
    cursor.close()
    conn.close()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity