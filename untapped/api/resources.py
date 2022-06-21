from typing import Optional, Any
from datetime import date

from pydantic import BaseModel
from fastapi import FastAPI, status, HTTPException
from email_validator import validate_email, EmailNotValidError

import logging
from untapped import models

from untapped.service import users, address as residence

app = FastAPI()


class CreateUser(BaseModel):
    first_name: str
    email: str
    password: str
    verified: Optional[int]

    class Config:
        orm_mode = True


class CreateUserResponse(CreateUser):
    id: int

    class Config:
        orm_mode = True


class EditUser(BaseModel):
    id: int
    middle_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: date = None
    nationality: Optional[str]
    phone_number: Optional[str]

    class Config:
        orm_mode = True


class CreateAddress(BaseModel):
    user_id: int
    country: str
    city: str
    state_or_province: Optional[str]
    zip_code: Optional[int]

    class Config:
        orm_mode = True


class CreateAddressResponse(CreateAddress):
    id: int

    class Config:
        orm_mode = True


@app.post("/register", response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
def create_users(user: CreateUser):
    """Create register user endpoint"""

    # perform email validation
    try:
        validate_email(user.email).email
    except EmailNotValidError as e:
        print(str(e))
        raise HTTPException(status_code=400, detail=str(e))

    # if we are here then email is valid
    new_user = models.User(
        first_name=user.first_name,
        email=user.email,
        password=user.password,
        verified=0
    )

    users.create_user(new_user)
    return new_user


@app.put("/edit-profile", response_model=EditUser, status_code=status.HTTP_200_OK)
def edit_user(user: EditUser):
    """edit profile"""

    # perform date validation

    updated_user = models.User(
        id=user.id,
        middle_name=user.middle_name,
        last_name=user.last_name,
        date_of_birth=user.date_of_birth,
        nationality=user.nationality,
        phone_number=user.phone_number
    )

    users.edit_user(updated_user)
    return updated_user


@app.post("/residence", response_model=CreateAddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(address: CreateAddress):
    """Create residential info"""

    new_address = models.Address(
        user_id=address.user_id,
        country=address.country,
        city=address.city,
        state_or_province=address.state_or_province,
        zip_code=address.zip_code
    )

    residence.create_address(new_address)
    return new_address


