from typing import *
from datetime import datetime
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    ID: int
    Product: str
    Price: int
    Tellno: str
    Address: str

class TelegramCreate(BaseModel):
    ID: int
    Date : datetime
    Channel_username: str
    Media_path : str
    Message : str  

class Detected_Image_Create(BaseModel):
    ID: int 
    label: str
    confidence: float
    Image : str
    x_max : float 
    x_min : float 
    y_max : float 
    y_min : float

class Product(BaseModel):
    ID: int = Field( alias="ID") 
    Price: Optional[int] = Field(None, alias="Price") 
    Product: str
    Tellno: str
    Address: str

    class Config:
        from_attributes=True

class Telegram(BaseModel):
    ID: int = Field(alias="ID") 
    Date : datetime
    Channel_username: str
    Media_path : str
    Message: Optional[str] = Field(None, alias="Message") 

    class Config:
        from_attributes=True

class Detected_Images(BaseModel):
    ID: int = Field(alias="ID")
    label: str
    confidence: float
    Image : str
    x_max : float 
    x_min : float 
    y_max : float 
    y_min : float