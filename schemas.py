"""
Database Schemas for Energy4You

Each Pydantic model corresponds to a MongoDB collection (lowercased class name).
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


class Lead(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    company: Optional[str] = Field(None, description="Company name")
    message: Optional[str] = Field(None, description="Message body")
    source: Optional[str] = Field("website", description="Lead source identifier")


class Newsletter(BaseModel):
    email: str = Field(..., description="Subscriber email")
    consent: bool = Field(True, description="GDPR consent")


class Project(BaseModel):
    title: str
    summary: str
    sector: str = Field(..., description="e.g., Residential, Industrial, Commercial, Public")
    location: Optional[str] = None
    capacity_kw: Optional[float] = Field(None, description="Installed capacity in kW")
    savings_percent: Optional[float] = Field(None, ge=0, le=100)
    image: Optional[HttpUrl] = None
    tags: List[str] = []


class BlogPost(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    cover_image: Optional[HttpUrl] = None
    author: Optional[str] = "Energy4You"
    published_at: Optional[datetime] = None
    tags: List[str] = []


class Testimonial(BaseModel):
    name: str
    role: Optional[str] = None
    quote: str
    avatar: Optional[HttpUrl] = None
