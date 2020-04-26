import secrets

from hashlib import sha256
from fastapi import Cookie, Depends, FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
app = FastAPI()
app.secret_key = "wjoirnfgojajw3ur902i4qoifjsoq0291i49823hwefjqh204u3y523aknsdajkbsdojwui"
security = HTTPBasic()
app.sessions = {}
templates = Jinja2Templates(directory="templates")


def auth_login(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}",
                                 encoding="utf8")).hexdigest()
    app.sessions[session_token] = credentials.username
    return session_token


@app.get("/login")
@app.post("/login")
def login(session_token: str = Depends(auth_login)):
    if session_token in app.sessions:
        response = RedirectResponse(url="/welcome")
        response.headers["location"] = "/welcome"
        response.set_cookie(key="session_token", value=session_token)
        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found",
            headers={"WWW-Authenticate": "Basic"},
        )


def check_session(session_token: str = Cookie(None)):
    if session_token not in app.sessions:
        session_token = None
    if session_token is None:
        raise HTTPException(status_code=401, detail="Access denied. Please log in first")
    return session_token


# @app.get("/logout", dependencies=[Depends(check_session)])
@app.post("/logout", dependencies=[Depends(check_session)])
def log_out(session_token: str = Depends(check_session)):
    app.sessions.pop(session_token)
    response = RedirectResponse(url="/")
    response.delete_cookie(key="session_token")
    return response


@app.get("/")
def root():
    return {"message": "Another Hello World"}


@app.get("/welcome", dependencies=[Depends(check_session)])
def get_welcome(request: Request, session_token: str = Depends(check_session)):
    username = app.sessions[session_token]
    return templates.TemplateResponse("welcome.html", {"request": request, "user": username})


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


app.count = 1
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


@app.post("/patient", dependencies=[Depends(check_session)])
def add_patient(patient_info: AddPatient):
    patient_id = str(app.count)
    app.patients_dic[patient_id] = patient_info
    counter_inc()
    response = RedirectResponse(url="/patient/{patient_id}")
    return response


@app.get("/patient/{patient_id}/", response_model=AddPatient, dependencies=[Depends(check_session)])
def pk_patient(patient_id: int):
    if str(patient_id) in app.patients_dic.keys():
        return app.patients_dic[str(patient_id)]
    else:
        raise HTTPException(status_code=204, detail="no_content")


@app.get("/patient", dependencies=[Depends(check_session)])
def get_all_patients():
    if len(app.patients_dic) > 0:
        return app.patients_dic

@app.delete("/patient/{patient_id}", dependencies=[Depends(check_session)])
def delete_patient(patient_id: str):
    if patient_id not in app.patients_dic.keys():
        raise HTTPException(status_code=204, detail="no_content")
    app.patients_dic.pop(patient_id)

