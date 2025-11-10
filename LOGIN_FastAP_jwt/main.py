"""
Aplicación FastAPI: Autenticación JWT y Gestión de Sesiones
-----------------------------------------------------------------------------

Propósito: Servidor backend que implementa un sistema básico de inicio de sesión 
y protección de rutas (Dashboard) utilizando JSON Web Tokens (JWT) y cookies.

Características clave:
1. Autenticación: Valida usuarios contra un diccionario de 'db de ejemplo'.
2. JWT: Genera un token de acceso con expiración de 60 segundos.
3. Rutas Protegidas: La ruta '/users/dashboard' requiere un 'access_token' 
    válido en las cookies.
4. Gestión de Sesiones: Utiliza cookies para almacenar y eliminar el token 
    de acceso al iniciar/cerrar sesión.

Dependencias: FastAPI, Jinja2Templates, jose (python-jose).
"""

from fastapi import FastAPI, Request, Form, HTTPException, Cookie
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timedelta
from jose import jwt, JOSEError, JWTError 
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

SECRETE_KEY= 'C7CwPTLRuufejqKASxXSg6cPgavBVaTAQzmHffAWsC8QFCKQ6V2j8GadIHKJK8gZ'
TOKEN_SECONDS_EXP = 60

#db de ejemplo
db_user = { 
    'saitama':{
        'id': 0,
        'username': 'saitama',
        'password': '12345#hash'
    },
    'genos':{
        'id': 1,
        'username': 'genos',
        'password': '54321#hash'
    }
}

jinja2_template = Jinja2Templates(directory='templates')

#comprobar si existe usuario
def get_user(username: str, db: list):
    if username in db:
        return db[username]

#comprobar si existe la password
def authenticate_user(password: str, password_plane: str):
    password_clean = password.split("#")[0]
    if password_plane == password_clean:
        return True
    return False


def create_token(data: list):
    data_token = data.copy()
    data_token["exp"] = datetime.utcnow() + timedelta(seconds=TOKEN_SECONDS_EXP)
    token_jwt = jwt.encode(data_token, key= SECRETE_KEY, algorithm="HS256")
    return token_jwt


@app.get('/', response_class=HTMLResponse)
def root(request: Request):
    return jinja2_template.TemplateResponse('index.html', {'request': request})

@app.get("/users/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, access_token: Annotated[str | None, Cookie()] = None):
    if  access_token  is None:
        return RedirectResponse('/', status_code=302)
    try:
        data_user = jwt.decode(access_token, key=SECRETE_KEY, algorithms=["HS256"])
        if get_user(data_user["username"], db_user) is None:
            return RedirectResponse("/", status_code=302)
        return jinja2_template.TemplateResponse("dashboard.html", {"request": request})
    except JWTError:
        return RedirectResponse("/", status_code=302)   


@app.post("/users/login")
def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user_data = get_user(username, db_user)
    if user_data is None:
        raise HTTPException(
            status_code=401,
            detail='No Authorization'
        )
    if not authenticate_user(user_data["password"], password):
        raise HTTPException(
            status_code=401,
            detail='No Authorization'
        )
    token = create_token({"username": user_data["username"]})
    return RedirectResponse(
        "/users/dashboard",
        status_code=302,
        headers={"set-cookie":f"access_token={token}; Max-Age={TOKEN_SECONDS_EXP}"})


@app.post("/users/logout")
def logout():
    return RedirectResponse("/", status_code=302, headers={
        "set-cookie": "access_token=; Max-Age=0"
    })


#Para activar el entorno virtual
#venv\Scripts\activate

#Para iniciar el servidor web
#uvicorn main:app --reload