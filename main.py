
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Another Hello World"}


@app.get("/method/")
def get_method():
    return {"method": "GET"}

@app.get("/welcome/")
def get_welcome():
    return {"message: Yet another welcome message"}

@app.post("/method/")
def post_method():
    return {"method": "POST"}


@app.put("/method/")
def put_method():
    return {"method": "PUT"}


@app.delete("/method/")
def delete_method():
    return {"method": "DELETE"}


app.count = 0
app.patients_dic = {}


def counter_inc():
    app.count += 1
    return app.count


class AddPatient(BaseModel):
    name: str
    surename: str


class ReturnPatient(BaseModel):
    id: str
    patient: AddPatient


@app.post("/patient/", response_model=ReturnPatient)
def add_patient(patient_info: AddPatient):
    patient_id = str(app.count)
    app.patients_dic[patient_id] = patient_info
    counter_inc()

    return ReturnPatient(id=app.count, patient=patient_info)


@app.get("/patient/{pk}/", response_model=AddPatient)
def pk_patient(pk: int):
    if str(pk) in app.patients_dic.keys():
        return app.patients_dic[str(pk)]
    else:
        raise HTTPException(status_code=204, detail="no_content")


