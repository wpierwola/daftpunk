from typing import Dict

from fastapi import FastAPI

from pydantic import BaseModel


app = FastAPI()


app.counter = 0
app.patients_dic = {}


@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/method/")
def get_method():
    return {"method": "GET"}


@app.put("/method/")
def put_method():
    return {"method": "PUT"}


@app.post("/method/")
def post_method():
    return {"method": "POST"}


@app.delete("/method/")
def delete_method():
    return {"method": "DELETE"}


def counter_inc():
    app.counter += 1
    return app.counter


class AddPatient(BaseModel):
    name: str
    surename: str


"""class ReturnPatient(BaseModel):
    id: int = app.counter
    patient_data = Dict"""


@app.post("/patient/")
def add_patient(patient_info: AddPatient):
    patient_id = app.counter
    app.patients_dic[patient_id] = patient_info.dict()
    counter_inc()
    return {"id": patient_id, "patient": patient_info.dict()}


