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
from recomendation_system import get_top_n_recommendations_model, recomendar_peliculas_calificadas
from models import User, Recommendation, Ratings, Movies, Tags, UserResponse, MoviesResponse, RecommendationResponse, RatingsResponse, TagsResponse, UserCreate


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


@app.post('/signup/', response_model=UserResponse)
def signup(user: UserCreate, db: db_dependency):
    existing_user = db.query(models.User).filter(models.User.user_id == user.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = models.User(user_id=user.user_id, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponse(user_id=db_user.user_id)  # Update as per your actual model fields


@app.get('/logout/')
def logout():
    return {'message': 'Logged out'}

@app.get('/users/', response_model=List[UserResponse])
def get_users(db: db_dependency):
    users = db.query(User).all()
    return users

@app.get('/users/{user_id}', response_model=models.UserResponse)
def get_user(user_id: str, db: db_dependency):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')

    # Make sure to return all required fields of the UserResponse model
    return UserResponse(
        user_id=user.user_id,
    )


@app.get('/recommendations/{user_id}', response_model=List[models.RecommendationResponse])
def get_recommendations(user_id: str, db: db_dependency):
    recommendations = db.query(models.Recommendation).filter(models.Recommendation.user_id == user_id).all()
    return recommendations


@app.get('/recommendations/', response_model=List[models.RecommendationResponse])
def get_recommendations(db: db_dependency):
    recommendations = db.query(models.Recommendation).all()
    return recommendations

@app.get('/movies/{movies_id}', response_model=MoviesResponse)
def get_movie(movies_id: str, db: db_dependency):
    movie = db.query(Movies).filter(Movies.movie_id == movies_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie not found')
    return MoviesResponse(
        movies_id=movie.movie_id,
        title=movie.title,
        stars=movie.stars or "",
        directors=movie.directors or "",
        genres=movie.genres
    )


@app.get('/movies/{movies_id}', response_model=models.MoviesResponse)
def movies(movie_id: str, db: db_dependency):
    movie = db.query(models.Business).filter(models.Movies.movie_id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie not found')
    return movie

@app.get('/ratings/', response_model=List[models.RatingsResponse])
def get_ratings(db: db_dependency):
    ratings = db.query(models.Ratings).all()
    return ratings

@app.get('/ratings/{rating_id}', response_model=models.RatingsResponse)
def get_rating(rating_id: int, db: db_dependency):
    rating = db.query(models.Ratings).filter(models.Ratings.rating_id == rating_id).first()
    if rating is None:
        raise HTTPException(status_code=404, detail='Rating not found')
    return rating


@app.get('/tags/', response_model=List[models.TagsResponse])
def get_tags(db: db_dependency):
    tags = db.query(models.Tags).all()
    return tags

@app.get('/tags/{tag_id}', response_model=TagsResponse)  # Corrected response_model
def get_tag(tag_id: int, db: db_dependency):
    tag = db.query(models.Tags).filter(models.Tags.tag_id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail='Tag not found')
    return tag

@app.get('/ratings/user/{user_id}', response_model=List[RatingsResponse])
def get_ratings_by_user(user_id: str, db: db_dependency):
    ratings = db.query(models.Ratings).filter(models.Ratings.user_id == user_id).all()
    if not ratings:
        raise HTTPException(status_code=404, detail='No ratings found for this user')
    return ratings

@app.get('/ratings/movies/{movie_id}', response_model=List[RatingsResponse])
def get_ratings_by_movie(movie_id: str, db: db_dependency):
    ratings = db.query(models.Ratings).filter(models.Ratings.movie_id == movie_id).all()
    if not ratings:
        raise HTTPException(status_code=404, detail='No ratings found for this business')
    return ratings


@app.get('/tags/user/{user_id}', response_model=List[TagsResponse])
def get_tags_by_user(user_id: str, db: db_dependency):
    tags = db.query(models.Tags).filter(models.Tags.user_id == user_id).all()
    if not tags:
        raise HTTPException(status_code=404, detail='No tags found for this user')
    return tags

@app.get('/tags/movies/{movie_id}', response_model=List[TagsResponse])
def get_tag_sby_movie(movie_id: str, db: db_dependency):
    tags = db.query(models.Tags).filter(models.Tags.movie_id == movie_id).all()
    if not tags:
        raise HTTPException(status_code=404, detail='No tags found for this business')
    return tags

@app.get('/recommendations/user/{user_id}', response_model=List[models.RecommendationResponse])
def get_top_n_recommendations(user_id: int, db: Session = Depends(get_db), top_n: int = 5):
    # # Check if user exists
    # user = db.query(User).filter(User.user_id == user_id).first()
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")

    recommendations = get_top_n_recommendations_model(user_id=user_id, top_n=top_n)
    print(recommendations)

    for rec in recommendations:
        movie_id = rec.iid  # Assuming rec is a Prediction object with movie_id as iid
        predicted_rating = rec.est  # Assuming rec is a Prediction object with predicted_rating as est

        new_rec = models.Recommendation(
            user_id=user_id,
            movie_id=movie_id,
            predicted_rating=predicted_rating  # Corrected field name
        )
        db.add(new_rec)
    db.commit()

    movie_ids = [rec.iid for rec in recommendations]  # Adjust index accordingly
    movies = db.query(models.Movies).filter(models.Movies.movie_id.in_(movie_ids)).all()
    movie_dict = {movie.movie_id: movie.title for movie in movies}

    recommendation_responses = []
    for rec in recommendations:
        recommendation_responses.append(models.RecommendationResponse(
            recommendation_id = db.query(func.max(Recommendation.id)).scalar() +1 or 0,
            user_id=user_id,
            movie_id=rec.iid,  # Adjust index accordingly
            predicted_rating=rec.est,  # Corrected field name
            movie_name=movie_dict.get(rec.iid, "Unknown")  # Adjust index accordingly
        ))
    return recommendation_responses




@app.get('/recommendations/user/graph/{user_id}', response_model=List[models.RecommendationResponse])
def get_top_n_recommendations_graph(user_id: int, movie_name: str, db: Session = Depends(get_db), top_n: int = 5):
    recommendations = recomendar_peliculas_calificadas(movie_title=movie_name, user_id=user_id, top_n=top_n)
    print(recommendations)

    for rec in recommendations:
        new_rec = models.Recommendation(
            user_id=user_id,
            rating=rec["predicted_rating"],
            movie_name=rec["movie_name"],
        )
        db.add(new_rec)
    db.commit()

    movie_names = [rec["movie_name"] for rec in recommendations]
    movies = db.query(models.Movies).filter(models.Movies.movie_name.in_(movie_names)).all()
    movie_dict = {movie.movie_name: movie.movie_id for movie in movies}

    recommendation_responses = []
    for rec in recommendations:
        recommendation_responses.append(models.RecommendationResponse(
            user_id=user_id,
            movie_id=movie_dict.get(rec["movie_name"], 0),
            rating=rec["predicted_rating"],
            movie_name=rec["movie_name"]
        ))
    return recommendation_responses

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)