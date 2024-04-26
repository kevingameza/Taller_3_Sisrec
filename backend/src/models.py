from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum
from database import Base
import enum
from pydantic import BaseModel
from sqlalchemy import ARRAY
from typing import List, Optional  # Importar List y Optional para el nuevo campo



class User(Base):
    __tablename__= 'users'
    
    user_id = Column(String, primary_key=True, index=True)
    password = Column(String)
    name = Column(String, nullable=True)
    
    
class Business(Base):
    __tablename__= 'business'
    
    business_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String, nullable=True)
    stars = Column(Float, index=True)
    postal_code = Column(Integer, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)



class Recomendation(Base):
    __tablename__= 'recomendations'
    
    recommendation_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    business_id = Column(String, ForeignKey('business.business_id'))
    stars = Column(Float)
    neighbors = Column(ARRAY(String), nullable=True) 
    

class Reviews(Base):
    __tablename__= 'reviews'

    review_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    business_id = Column(String, ForeignKey('business.business_id'))
    stars = Column(Float)
    text = Column(String, nullable=True)
    date = Column(String, nullable=True)

class UserResponse(BaseModel):
    user_id: str
    name: str
    
class BusinessResponse(BaseModel):
    business_id: str
    name: str
    address: str
    stars: float
    postal_code: int
    latitude: float
    longitude: float


class RecomendationResponse(BaseModel):
    id: int
    user_id: str
    business_id: str
    stars: float
    neighbors: Optional[List[str]] = None
    
    
class ReviewsResponse(BaseModel):
    review_id: str
    user_id: str
    business_id: str
    stars: float
    text: str
    date: str
