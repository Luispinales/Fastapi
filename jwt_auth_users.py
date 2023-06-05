from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str 
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "luisP": {
    "username": "luisP",
    "full_name": "Luis Pinales",
    "email": "Luispamparo13@gmail.com",
    "disabled": False,
    "password": "$2a$12$iosblVox7gXKSfuDFyO2X.rmNGkUuCtBU5n9W0GbnxGYsTB7CCyQW"
},    
     "luisp2": {
    "username": "luisP2",
    "full_name": "Luis Pinales2",
    "email": "Luispamparo13@gmail.com2",
    "disabled": True,
    "password": "$2a$12$d5AKB6PhBpBIpXfvG7cNw.Xv3vh7WdrpbTIWhBwRnV6Ky8ztY1arG"
}

}



def search_user_db(username: str = Depends(oauth2)):
    if username in users_db: 
        return UserDB(**users_db[username])
    

def search_user(username: str = Depends(oauth2)):
    if username in users_db: 
        return User(**users_db[username])
    
    

async def auth_user(token: str = Depends(oauth2)):
   exception = HTTPException(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        detail= "Credenciales de autetificacion invalidas")

    

   try: 
     username = jwt.decode(token, SECRET, ALGORITHM).get("sub")
     if username is None:
         raise exception



   except JWTError:
        raise exception

   return search_user(username)

async def current_user(user: User= Depends(auth_user)):
    if not user: 
     raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail= "Credenciales de autetificacion invalidas")
    return user  



@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db: 
      raise HTTPException(
        status_code=status.HTTP_418_IM_A_TEAPOT, detail= "el usuario no existe") 
    

    user = search_user_db(form.username)

    crypt.verify(form.password, user.password)

    if not  crypt.verify(form.password, user.password):
         raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT , detail= "la password no es correcta")
    
    access_token = {"sub": user.username, 
                   "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return{"access_token": jwt.encode(access_token, SECRET, algorithm = ALGORITHM), "token_type": "bearer"}



@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user 



  
uvicorn.run(app, port=1000)
