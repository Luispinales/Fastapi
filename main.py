from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users
import uvicorn
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")





@app.get("/")
async def root():
    return "Hola FastAPI" 

@app.get("/url")
async def root():
    return ("url:" "Https:luisPamparo")


@app.post("/")
async def root():
    return







uvicorn.run(app, port=1000)
