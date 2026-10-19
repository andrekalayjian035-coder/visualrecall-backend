import os

import mysql.connector
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

app = FastAPI(title="VisualRecall API")


@app.get("/")
def home():
    return {"message": "FastAPI is working"}


@app.get("/db-test")
def database_test():
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=os.environ["MYSQLHOST"],
            port=int(os.environ["MYSQLPORT"]),
            user=os.environ["MYSQLUSER"],
            password=os.environ["MYSQLPASSWORD"],
            database=os.environ["MYSQLDATABASE"],
        )

        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE(), NOW()")
        database_name, current_time = cursor.fetchone()

        return {
            "message": "Database connection works",
            "database": database_name,
            "server_time": str(current_time),
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not connect to the database",
        )

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()