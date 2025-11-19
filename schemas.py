"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# ------------------------------
# Real Estate: Hyderabad
# ------------------------------

class Property(BaseModel):
    """
    Properties collection schema
    Collection name: "property"
    """
    title: str = Field(..., description="Listing title")
    description: Optional[str] = Field(None, description="Short description")
    price_in_inr: int = Field(..., ge=0, description="Price in INR")
    location: str = Field(..., description="Locality/Area in Hyderabad")
    city: str = Field("Hyderabad", description="City")
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[int] = Field(None, ge=0)
    area_sqft: Optional[int] = Field(None, ge=0)
    property_type: str = Field(..., description="Apartment, Villa, Plot, Commercial")
    amenities: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    status: str = Field("available", description="available, booked, sold")

class Inquiry(BaseModel):
    """
    Inquiries (leads) collection schema
    Collection name: "inquiry"
    """
    name: str = Field(..., description="Full name of lead")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    message: Optional[str] = Field(None, description="Message from lead")
    interested_location: Optional[str] = Field(None, description="Area of interest in Hyderabad")
    budget_in_inr: Optional[int] = Field(None, ge=0)
    property_type: Optional[str] = Field(None)
    source: str = Field("website", description="Lead source")

# Example schemas (kept for reference)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
