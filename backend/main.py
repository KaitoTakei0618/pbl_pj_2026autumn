import os

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar_one()

        return {
            "status": "ok",
            "result": result,
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )