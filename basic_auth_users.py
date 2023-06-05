from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")



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
    "password": "123456"
},    
     "luisp2": {
    "username": "luisP2",
    "full_name": "Luis Pinales2",
    "email": "Luispamparo13@gmail.com2",
    "disabled": True,
    "password": "654321"
}

}

def search_user_db(username: str):
    if username in users_db: 
        return UserDB(**users_db[username])
    

    
def search_user(username: str):
    if username in users_db: 
        return User(**users_db[username])



async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:  raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail= "Credenciales de autetificacion invalidas")
    return user  



@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db: 
      raise HTTPException(
        status_code=status.HTTP_418_IM_A_TEAPOT, detail= "el usuario no existe") 
    

    user = search_user_db(form.username)
    if not form.password == user.password:
         raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT , detail= "la password no es correcta")
    
    return{"access_token": user.username, "token_type": "bearer"}



@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


uvicorn.run(app, port=1000)
