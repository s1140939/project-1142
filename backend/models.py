from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base


class Laptop(Base):

    __tablename__ = "laptops"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id = Column(
        String,
        unique=True,
        index=True,
        nullable=True
    )

    name = Column(
        String,
        nullable=False
    )

    brand = Column(
        String,
        nullable=True
    )

    cpu = Column(
        String,
        nullable=True
    )

    ram = Column(
        String,
        nullable=True
    )

    ssd = Column(
        String,
        nullable=True
    )

    price = Column(
        Integer,
        nullable=True
    )

    url = Column(
        String,
        nullable=True
    )

    updated_at = Column(
        DateTime,
        default=datetime.now
    )