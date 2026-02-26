from sqlalchemy import Column, Integer, String, Date
from database import Base

class Application(Base):
    """
    Represents a job app in the tracker 
    Maps to the 'application' table in Postgresql 
    
    """
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True) # indexed for faster lookups 
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Applied") # tracks pipeline stage: Applied, Phone Screen, Interview, Offer, Rejected
    date_applied = Column(Date, nullable=False)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)