from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True, nullable=False)
    firstname = Column(String, index=True, unique=True, nullable=False)
    number_guests = Column(Integer, index=True, nullable=False)
    is_present = Column(Boolean, index=True, nullable=False)
    message = Column(String, index=True)
