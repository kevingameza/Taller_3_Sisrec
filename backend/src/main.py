from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import models
from database import sessionLocal, engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
import uvicorn
from pydantic import BaseModel
from typing import List, Annotated
import enum

from models import User, Recomendation, Reviews, Business, UserResponse, BusinessResponse, RecomendationResponse, ReviewsResponse
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "PATCH"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
db_dependency = Annotated[Session, Depends(get_db)] 


@app.get('/')
def read_root():
    return {'message': 'Hello World'}


class User(BaseModel):
    user_id: str
    password: str
    name: str


@app.post('/signup/', response_model=UserResponse)
def signup(user: User, db: db_dependency):
    existing_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = models.User(user_id=user.user_id, password=user.password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse(user_id=db_user.user_id, name=db_user.name)


@app.post('/login/', response_model=models.UserResponse)
def login(user: User, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    if db_user.password != user.password:
        raise HTTPException(status_code=401, detail='Invalid password')
    return db_user

@app.get('/logout/')
def logout():
    return {'message': 'Logged out'}

@app.get('/users/', response_model=List[models.UserResponse])
def get_users(db: db_dependency):
    users = db.query(models.User).all()
    return users

@app.get('/users/{user_id}', response_model=models.UserResponse)
def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user







if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)