from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, Date, func, ForeignKey,extract,cast, DATE
from sqlalchemy.orm import sessionmaker, declarative_base, Session, joinedload,relationship
from databases import Database
from typing import List, Dict, Any
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


DATABASE_URL = "postgresql://postgres:0000@localhost:5432/farcal_db"

# SQLAlchemy models
Base = declarative_base()

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

# Enable CORS for all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        raise HTTPException(status_code=404, detail="Crop not found")

    period = db.query(AgriculturalPeriod).filter(AgriculturalPeriod.startdate <= date, AgriculturalPeriod.enddate >= date).first()
    if not period:
        raise HTTPException(status_code=404, detail="Agricultural period not found for the given date")

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