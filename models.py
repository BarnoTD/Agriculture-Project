from pydantic import BaseModel

class FarmProfile(BaseModel):
    id: int
    location: str
    crops: str

class User(BaseModel):
    id: int
    username: str
    email: str
    farm_profile: FarmProfile
