from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

# 🔹 Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows all origins (good for development)
    allow_credentials=True,
    allow_methods=["*"],  # allows all HTTP methods: GET, POST, etc.
    allow_headers=["*"],  # allows all headers
)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="bmi_app"
    )


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/search")
def search(height: float, weight: float):
    bmi = round(weight / (height * height), 2)

    if bmi < 18.5:
        status = "underweight"
        correct_bmi = round(18.5 * (height * height), 2)
        needToGain = round(correct_bmi - weight, 2)
        result = {
            "bmi": bmi,
            "status": status,
            "correct_bmi": correct_bmi,
            "needToGain": needToGain
        }

    elif 18.5 <= bmi <= 24.9:
        status = "normal"
        result = {
            "bmi": bmi,
            "status": status
        }

    elif bmi> 24:
        status = "overweight"
        correct_bmi = round(24.9 * (height * height), 2)
        needToLose = round(weight - correct_bmi, 2)
        result = {
            "bmi": bmi,
            "status": status,
            "correct_bmi": correct_bmi,
            "needToLose": needToLose
        }

   
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO bmi_records (height, weight, bmi, status) VALUES (%s, %s, %s, %s)"
        values = (height, weight, bmi, status)
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Record inserted successfully!")
    except mysql.connector.Error as err:
        print(f"❌ Error inserting record: {err}")

    return result


@app.get("/records")

def get_records():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bmi_records ORDER BY created_at DESC")
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
    except mysql.connector.Error as err:
        print(f"❌ Error fetching records: {err}")
        return {"error": str(err)}

