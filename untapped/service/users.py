from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from fastapi import FastAPI, HTTPException

from untapped.database import SessionLocal
from untapped.models import User

db = SessionLocal()


def create_user(user):
    """Add a new user record to the users table"""
    print("Service layer...")
    try:
        db.add(user)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail="A user with that email already exists")


def edit_user(profile):
    """
    :param profile: the details of the user to be updated
    :return:
    """
    try:
        user = db.query(User).get(profile.id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"No user with id: {profile.id}")
        user.nationality = profile.nationality
        user.middle_name = profile.middle_name
        user.last_name = profile.last_name
        user.phone_number = profile.phone_number
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
