import secrets

from hashlib import sha256
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from pydantic import BaseModel
from typing import Dict

app = FastAPI()
app.secret_key = "wjoirnfgojajw3ur902i4qoifjsoq0291i49823hwefjqh204u3y523aknsdajkbsdojwuirfhuihnfbasjnfbsfihfbrhqwihsdjvbgeh0912u43289hfkjnwo203urhsijfe90ry2gh9shfusd"
security = HTTPBasic()
app.sessions = {}


@app.get("/")
def root():
    return {"message": "Another Hello World"}


@app.get("/method/")
def get_method():
    return {"method": "GET"}


@app.get("/welcome")
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


def auth_login(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding = "utf8")).hexdigest()
    app.sessions[session_token] = credentials.username
    return session_token


@app.get("/login/")
@app.post("/login/")
def login(response: Response, session_token: str = Depends(auth_login)):
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/welcome"
    response.set_cookie(key="session_token", value=session_token)


