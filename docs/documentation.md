# FastAPI User Creation API

This is a simple FastAPI application for creating users with their names and emails and storing them in a database.

## Dependencies

- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

- SQLAlchemy: The Python SQL Toolkit and Object-Relational Mapper that gives application developers the full power and flexibility of SQL.

- Pydantic: Data validation and settings management using Python type annotations.

To install these dependencies, run the following command:

```bash
pip install fastapi sqlalchemy pydantic
```

## User Model

The User model is a Pydantic model that contains the structure of the user data including `name` and `email`. Both fields are of string type.

```python
class User(BaseModel):
    name: str
    email: str
```

## API Endpoints

### POST /users/

This endpoint is used to create a user.

#### Parameters

- `user`: a JSON object containing `name` and `email` fields.

#### Example

Request:

```bash
curl -X POST "http://localhost:8000/users/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"name\":\"John\",\"email\":\"john@example.com\"}"
```

Response:

```json
{
  "message": "User created"
}
```

#### Note

This endpoint will return a `400 Bad Request` HTTP response in case of any database operation error.

```python
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
```

## Database

This API uses SQLite as a database. The connection string for the database is 'sqlite:///./test.db'. To change the database, replace this string with the connection string of your chosen database.

```python
engine = create_engine('sqlite:///./test.db')
metadata = MetaData(bind=engine)
```