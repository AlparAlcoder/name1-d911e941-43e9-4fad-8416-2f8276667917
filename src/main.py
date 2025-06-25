from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()
engine = create_engine('sqlite:///./test.db')
metadata = MetaData(bind=engine)

class User(BaseModel):
    name: str
    email: str

@app.post("/users/")
async def create_user(user: User):
    try:
        users = Table('users', metadata, autoload=True)
        insert = users.insert().values(name=user.name, email=user.email)
        conn = engine.connect()
        conn.execute(insert)
        conn.close()
        return {"message": "User created"}
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Error on database operation")