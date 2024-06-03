from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum
from database import Base
import enum
from pydantic import BaseModel, Field
from sqlalchemy import ARRAY
from typing import List, Optional  # Importar List y Optional para el nuevo campo

class User(Base):
    __tablename__= 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    password = Column(String)
    
class UserCreate(BaseModel):
    user_id: int
    password: str

class UserResponse(BaseModel):
    user_id: int
    name: str
    
    class Config:
        orm_mode = True

class Movies(Base):
    __tablename__= 'movies'
    
    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genres = Column(String, index=True)
    stars = Column(String, nullable=True)
    directors = Column(String, nullable=True)
    startYear = Column(Integer, nullable=True)
    isAdult = Column(Boolean, nullable=True)


class Recommendation(Base):
    __tablename__ = 'recommendations'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    movie_id = Column(Integer, ForeignKey('movies.movie_id'))
    predicted_rating = Column(Float, nullable=True)  # Ensure this is correctly named
    movie_name = Column(String, index=True)
    

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
    user_id: int

    class Config:
        orm_mode = True
class MoviesResponse(BaseModel):
    movies_id: int
    title: str
    stars: Optional[str] = Field(default=None)
    directors: Optional[str] = Field(default=None)
    genres: str
    starYear: Optional[int] = Field(default=None)
    isAdult: Optional[bool] = Field(default=None)


class RecommendationResponse(BaseModel):
    recommendation_id: int
    user_id: int
    movie_id: int
    predicted_rating: float
    movie_name: str


    
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