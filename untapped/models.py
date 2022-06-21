# from database import Base
from untapped.database import Base
from sqlalchemy import String, Integer, Date, Column, ForeignKey


class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    verified = Column("verified", Integer, nullable=True, default=0)
    password = Column("password", String, nullable=False)
    middle_name = Column("middle_name", String, nullable=True)
    last_name = Column("last_name", String, nullable=True)
    date_of_birth = Column("date_of_birth", Date, nullable=True)
    nationality = Column("nationality", String, nullable=True)
    phone_number = Column("phone_number", String, nullable=True)

    def __repr__(self):
        # TODO - add all other user properties (apart from password)
        return f"<User first_name={self.first_name} email={self.email}>"


class Address(Base):
    __tablename__ = "address"
    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("users.id"), unique=True)
    country = Column("country", String, nullable=False)
    city = Column("city", String, nullable=False)
    state_or_province = Column("state_or_province", String, nullable=True)
    zip_code = Column("zip_code", Integer, nullable=True)

    def __repr__(self):
        return f"<Address country={self.country} city={self.city}>"
