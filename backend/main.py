
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

from database import get_session

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/db-check")
def db_check(session: Session = Depends(get_session)):
    try:
        result = session.exec(text("SELECT 1")).scalar_one()

        return {
            "status": "ok",
            "result": result,
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )
