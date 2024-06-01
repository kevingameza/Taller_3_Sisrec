from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum
from database import Base
import enum
from pydantic import BaseModel
from sqlalchemy import ARRAY
from typing import List, Optional  # Importar List y Optional para el nuevo campo

class User(Base):
    __tablename__= 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    
    
class Movies(Base):
    __tablename__= 'movies'
    
    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    stars = Column(String, nullable=True)
    directors = Column(String, index=True)
    genres = Column(String, index=True)



class Recommendation(Base):
    __tablename__= 'recommendations'
    
    recommendation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    stars = Column(Float, index=True)
    

class Ratings(Base):
    __tablename__= 'ratings'

    rating_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    rating = Column(Float)

class Tags(Base):
    __tablename__ = 'tags'

    tag_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    tag = Column(String)

class UserResponse(BaseModel):
    user_id: str
    name: str
    
class MoviesResponse(BaseModel):
    movies_id: int
    title: str
    stars: str
    directors: str
    genres: str

class RecommendationResponse(BaseModel):
    recommendation_id: int
    user_id: str
    movie_id: str
    stars: float
    
class RatingsResponse(BaseModel):
    rating_id: int
    user_id: int
    movie_id: int
    rating: float

class TagsResponse(BaseModel):
    tag_id: int
    user_id: int
    movie_id: int
    tag: str