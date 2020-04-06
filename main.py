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



@app.post("/method/")
def post_method():
    return {"method": "POST"}


@app.put("/method/")
def put_method():
    return {"method": "PUT"}


@app.delete("/method/")
def delete_method():
    return {"method": "DELETE"}


def counter_inc():
    app.counter += 1
    return app.counter


class AddPatient(BaseModel):
    name: str
    surename: str


class ReturnPatient(BaseModel):
    id: int
    patient_data: AddPatient


@app.post("/patient/", response_model = ReturnPatient)
def add_patient(patient_info=AddPatient):
    patient_id = app.counter
    app.patients_dic[patient_id] = patient_info
    counter_inc()

    return ReturnPatient(id=app.counter, patient_data=patient_info)

