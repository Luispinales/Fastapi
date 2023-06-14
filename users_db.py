from fastapi import APIRouter, HTTPException, status
from db.models.users import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId


router = APIRouter(prefix= "/userdb",
                   tags= ["/userdb"],
                   responses= {status.HTTP_418_IM_A_TEAPOT: {"message": "No encontrado"}})

# Entidad user


@router.get("/",response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())


 
#Path
@router.get("/{id}")
async def user(id:str):
    return search_user("_id",ObjectId(id))

#Query
@router.get("/")
async def user(id:str):
    return search_user("_id",ObjectId(id))


@router.post("/", status_code=201)
async def user(user: User):
 if type(search_user("email",user.email)) == User:  #aqui metemos el user.id como parametro y como criterio de lo que haremos
    raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail= "el usuario ya existe")
     
       
 user_dict = dict(user)

 id = db_client.local.users.insert_one(user_dict).inserted_id
 del user_dict["id"]


 new_user = user_schema(db_client.local.users.find_one({"_id": id})) # este es el criterio para buscar el id

 return User(**new_user)



found = False  


@router.put("/", response_model=User)
async def user(user: User): #aqui le enviamos el usuario completo, se lo pasamos todo y asi sabemos que vamos a actualizar
   
   user_dict = dict(user)
   del user_dict["id"]

   try:  
         db_client.local.users.find_one_and_replace(
        {"_id": ObjectId(user.id)}, user_dict)
   except:
    return {"error": "No se ha actualizado el usuario"}
   
   return search_user("_id", ObjectId(user.id))



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id:str):

     found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})

     if not found: 
      return{"error": "no se ha encontrado el usuario"}
   

def search_user(field: str, key):
   
    try:
      user = db_client.local.users.find_one({field: key}) # este es el criterio de email al igual que el de id
      return User(**user_schema(user))
    except:
     return {"error": "No se ha encontrado el usuario"}
    
     
     
     
'''
@router.put("/")
async def user(user: User): #aqui le enviamos el usuario completo, se lo pasamos todo y asi sabemos que vamos a actualizar
    for index, saved_user in enumerate(users_list): #vamos a recorrer la lista y si encontamos el usuario que nos estan dando pues la este se va a actualizar
     if saved_user.id == user.id: #si el ussuario guardado que es saved_id su id es == al user.id el usuario que tenemos, aqui ya deberia de eecir quer ya tenemos el usuario 
        users_list[index] = user #aqui es por sis acaso  no encontramos el usuario 
        found = True 
        
        if not found: 
          raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT, detail="Error: esto no se ha actualizado")
    return user

'''