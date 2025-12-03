from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    owner = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
