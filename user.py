def user_schema(user) -> dict:
    return {"id": str (user["_id"]),
           "username": user["username"],
           "email": user["email"]}


    _id: str | None
    username: str
    email: str 

def users_schema(users) -> list: 
    return [user_schema(user) for user in users]