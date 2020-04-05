from typing import Dict

from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/method/")
def get_method():
    return {"method": "GET"}


@app.post("/method/")
def get_method():
    return {"method": "POST"}


@app.put("/method/")
def get_method():
    return {"method": "PUT"}


@app.delete("/method/")
def get_method():
    return {"method": "DELETE"}
