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
from recomendation_system import get_recommendation, get_top_n_recommendations
from models import User, Recommendation, Reviews, Business, UserResponse, BusinessResponse, RecommendationResponse, ReviewsResponse
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
def get_user(user_id: str, db: db_dependency):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@app.get('/recommendations/{user_id}', response_model=List[models.RecommendationResponse])
def get_recommendations(user_id: str, db: db_dependency):
    recommendations = db.query(models.Recommendation).filter(models.Recommendation.user_id == user_id).all()
    return recommendations


@app.get('/recommendations/', response_model=List[models.RecommendationResponse])
def get_recommendations(db: db_dependency):
    recommendations = db.query(models.Recommendation).all()
    return recommendations

@app.get('/businesses/', response_model=List[models.BusinessResponse])
def get_businesses(db: db_dependency):
    businesses = db.query(models.Business).all()
    return businesses

@app.get('/businesses/{business_id}', response_model=models.BusinessResponse)
def get_business(business_id: str, db: db_dependency):
    business = db.query(models.Business).filter(models.Business.business_id == business_id).first()
    if business is None:
        raise HTTPException(status_code=404, detail='Business not found')
    return business

@app.get('/reviews/', response_model=List[models.ReviewsResponse])
def get_reviews(db: db_dependency):
    reviews = db.query(models.Reviews).all()
    return reviews

@app.get('/reviews/{review_id}', response_model=models.ReviewsResponse)
def get_review(review_id: int, db: db_dependency):
    review = db.query(models.Reviews).filter(models.Reviews.review_id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail='Review not found')
    return review

@app.get('/reviews/user/{user_id}', response_model=List[ReviewsResponse])
def get_reviews_by_user(user_id: str, db: db_dependency):
    reviews = db.query(models.Reviews).filter(models.Reviews.user_id == user_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail='No reviews found for this user')
    return reviews

@app.get('/reviews/business/{business_id}', response_model=List[ReviewsResponse])
def get_reviews_by_business(business_id: str, db: db_dependency):
    reviews = db.query(models.Reviews).filter(models.Reviews.business_id == business_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail='No reviews found for this business')
    return reviews

@app.get('/reviews/user/{user_id}/business/{business_id}', response_model=List[ReviewsResponse])
def get_reviews_by_user_and_business(user_id: str, business_id: str, db: db_dependency):
    reviews = db.query(models.Reviews).filter(models.Reviews.user_id == user_id, models.Reviews.business_id == business_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail='No reviews found for this user and business combination')
    return reviews

@app.get('/generate_recommendation/{user_id}/{business_id}', response_model=RecommendationResponse)
def generate_recommendation(user_id: str, business_id: str, db: db_dependency):
    recommendation = get_recommendation(user_id, business_id)
    db_recommendation = models.Recommendation(user_id=user_id, business_id=business_id, stars=recommendation)
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation

@app.get('/generate_top_n_recommendations/{user_id}', response_model=List[RecommendationResponse])
def generate_top_n_recommendations(user_id: str, db: db_dependency):
    recommendations = get_top_n_recommendations(user_id)
    db_recommendations = [models.Recommendation(user_id=recommendation.user_id,
                                                business_id=recommendation.business_id,
                                                stars=recommendation.stars) for recommendation in recommendations]
    db.add_all(db_recommendations)
    db.commit()
    return db_recommendations

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)