from unittest import result
import uuid
import uvicorn
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from postgres import PostgresConnection
from create_tables import create_tables

create_tables()

class User(BaseModel):
    username: str
    password: str

class Case(BaseModel):
    sc_submitted_by: str
    sc_name: str
    sc_age: int
    sc_gender: str
    sc_last_seen_location: str
    sc_case_status: str
    sc_case_image: str
    sc_face_encoding: str

app = FastAPI()

def get_user_id(username):
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("select u_id from users where u_name = '{}'".format(username))
        user_id = cursor.fetchone()
        return user_id[0]

def get_user_name(user_id):
    with PostgresConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("select u_name from users where u_id = '{}'".format(user_id))
        user_name = cursor.fetchone()
        return user_name[0]

@app.post('/login')
def authenticate(user: User):
    with PostgresConnection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE u_name = %s", (user.username,))
            result = cur.fetchone()
            if result:
                if result[2] == user.password:
                    return {"status": "success", "message": "Login successful"}
                else:
                    return {"status": "pass_error", "message": "Incorrect password"}
            else:
                return {"status": "error", "message": "User does not exist"}
    

@app.post("/register")
def register(user: User):
    with PostgresConnection() as connection:
        cursor = connection.cursor()
        cursor.execute("select * from users where u_name = '{}'".format(user.username))
        if cursor.fetchone():
            return {"status": "error", "message": "User already exists"}
        cursor.execute("insert into users (u_id, u_name, u_password) values ('{}', '{}', '{}')".format(
            str(uuid.uuid4()), user.username, user.password))
        return {"status": "success", "message": "User registered successfully"}

@app.post("/submit-case")
def submit_case(case: Case):
    user_id = get_user_id(case.sc_submitted_by)
    with PostgresConnection() as connection:
        cursor = connection.cursor()
        cursor.execute("insert into submitted_cases (sc_id, sc_submitted_by, sc_name, sc_age, sc_gender, sc_last_seen_location, sc_case_status, sc_case_image, sc_face_encoding) values ('{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', '{}')".format(
            str(uuid.uuid4()), user_id, case.sc_name, case.sc_age, case.sc_gender, case.sc_last_seen_location, case.sc_case_status, case.sc_case_image, case.sc_face_encoding))
        return {"status": "success", "message": "Case submitted successfully"}

@app.get("/get-cases")
def get_cases():
    with PostgresConnection() as connection:
        cursor = connection.cursor()
        cursor.execute("select * from submitted_cases")
        cases = cursor.fetchall()
        return cases

@app.get("/get-encodings")
def get_encodings():
    with PostgresConnection() as connection:
        cursor = connection.cursor()
        cursor.execute("select sc_face_encoding from submitted_cases")
        encodings = cursor.fetchall()
        return encodings

@app.post("/add-detected-person")
def add_detected_person(case_id: str, location: str):
    with PostgresConnection() as connection:
        cursor = connection.cursor()
        cursor.execute("insert into detected_persons (dp_id, dp_case_id, dp_location) values ('{}', '{}', '{}')".format(
            str(uuid.uuid4()), case_id, location))
        cursor.execute("update submitted_cases set sc_case_status = 'detected' where sc_id = '{}'".format(case_id))
        return {"message": "Detected person added successfully"}

@app.get("/get-detected-persons")
def get_detected_persons():
    with PostgresConnection() as connection:
        cursor = connection.cursor()
        cursor.execute("select * from detected_persons")
        detected_persons = cursor.fetchall()
        return detected_persons

if __name__ == "__main__":
    create_tables()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")