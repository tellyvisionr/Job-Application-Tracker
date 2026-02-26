from fastapi import FastAPI
from database import Base, engine
from models import Application

Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.post("/applications/")
async def create_applications():
    return Application







