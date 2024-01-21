from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, Date, func, ForeignKey, extract, cast, DATE
from sqlalchemy.orm import sessionmaker, declarative_base, Session, joinedload, relationship
from databases import Database
from typing import List, Dict, Any
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
import logging


DATABASE_URL = "postgresql://postgres:0000@localhost:5432/farcal_db"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# SQLAlchemy models
Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Crop(Base):
    __tablename__ = "crops"
    cropid = Column(Integer, primary_key=True, index=True)
    cropname = Column(String, index=True)
    
    # Add this relationship with an explicit join condition
    suggestions = relationship(
        "Suggestion",
        back_populates="crop",
        primaryjoin="Crop.cropid == foreign(Suggestion.cropid)"
    )


class AgriculturalPeriod(Base):
    __tablename__ = "agriculturalperiods"
    periodid = Column(Integer, primary_key=True, index=True)
    periodname = Column(String, index=True)
    startdate = Column(Date)  
    enddate = Column(Date)    

    # Add this relationship
    suggestions = relationship("Suggestion", back_populates="agricultural_period")

class Suggestion(Base):
    __tablename__ = "suggestions"
    suggestionid = Column(Integer, primary_key=True, index=True)
    cropid = Column(Integer, ForeignKey('crops.cropid'), index=True)
    periodid = Column(Integer, ForeignKey('agriculturalperiods.periodid'), index=True)  # Add this line
    proposal = Column(String)

    # Add these relationships
    crop = relationship("Crop", back_populates="suggestions")
    agricultural_period = relationship("AgriculturalPeriod", back_populates="suggestions")


class SuggestionResponse(BaseModel):
    suggestionid: int
    cropid: int
    periodid: int
    proposal: str

class AvailableSuggestionsResponse(BaseModel):
    crop_name: str
    period_name: str
    suggestions: List[SuggestionResponse]

class TokenRequest(BaseModel):
    username: str
    password: str

# Database instance
database = Database(DATABASE_URL)

# SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI app
app = FastAPI()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Secret key to sign JWT tokens
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Token expiration time (e.g., 15 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Enable CORS for all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User Registration
def register_user(db: Session, username: str, password: str):
    hashed_password = pwd_context.hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user and pwd_context.verify(password, db_user.hashed_password):
        return db_user


@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/token")
def login_for_access_token(request: TokenRequest, db: Session = Depends(get_db)):
    logging.info(f"Received login request for username: {request.username}")

    user = db.query(User).filter(User.username == request.username).first()
    if not user or not bcrypt.checkpw(request.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        logging.error("Invalid credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": "This is a protected route", "user": current_user}


# API endpoint to get all crops from the database
@app.get("/crops/", response_model=List[Dict[str, Any]])
async def read_crops(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = "SELECT * FROM crops OFFSET :skip LIMIT :limit"
    values = {"skip": skip, "limit": limit}
    result = db.execute(query, values)
    
    # Convert each row to a dictionary
    crops = [dict(row) for row in result.fetchall()]
    
    return crops

# API endpoint to get all agricultural periods from the database
@app.get("/agriculturalperiods/", response_model=List[Dict[str, Any]])
async def read_agricultural_periods(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = "SELECT * FROM agriculturalperiods OFFSET :skip LIMIT :limit"
    values = {"skip": skip, "limit": limit}
    result = db.execute(query, values)
    
    # Convert each row to a dictionary
    agricultural_periods = [dict(row) for row in result.fetchall()]
    
    return agricultural_periods

def get_available_suggestions(crop_name: str, date: str, db: Session):
    crop = db.query(Crop).filter(func.lower(Crop.cropname) == func.lower(crop_name)).first()
    if not crop:
        raise HTTPException(status_code=404, detail="لا وجود للمحصول في قاعدة البيانات")

    period = db.query(AgriculturalPeriod).filter(AgriculturalPeriod.startdate <= date, AgriculturalPeriod.enddate >= date).first()
    if not period:
        raise HTTPException(status_code=404, detail="لا توجد اقتراحات لمحصولكم في تلك الفترة")

    suggestions = (
        db.query(Suggestion)
        .filter(Suggestion.cropid == crop.cropid, Suggestion.periodid == period.periodid)
        .options(joinedload(Suggestion.crop), joinedload(Suggestion.agricultural_period))
        .all()
    )

    # Convert suggestions to a list of dictionaries
    suggestions_list = [
        {
            "suggestionid": suggestion.suggestionid,
            "cropid": suggestion.cropid,
            "periodid": suggestion.periodid,
            "proposal": suggestion.proposal,
            "periodname": suggestion.agricultural_period.periodname,  # Include period name
            # Add other fields as needed
        }
        for suggestion in suggestions
    ]

    # Return a JSONResponse with the list of suggestions
    return JSONResponse(content=suggestions_list)



# API endpoint to get all suggestions from the database
@app.get("/all_suggestions/", response_model=List[Dict[str, Any]])
async def read_all_suggestions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = "SELECT * FROM suggestions OFFSET :skip LIMIT :limit"
    values = {"skip": skip, "limit": limit}
    result = db.execute(query, values)
    
    # Convert each row to a dictionary
    suggestions = [dict(row) for row in result.fetchall()]
    
    return suggestions

@app.get("/available_suggestions/", response_model=AvailableSuggestionsResponse)
async def read_available_suggestions(crop_name: str, date: str, db: Session = Depends(get_db)):
    result = get_available_suggestions(crop_name, date, db)
    return result