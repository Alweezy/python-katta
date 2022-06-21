from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import FastAPI, HTTPException

from untapped.database import SessionLocal

db = SessionLocal()


def create_address(address):
    """Add a new address record to the users table"""
    try:
        db.add(address)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"An address for user {address.user_id} already exists")
