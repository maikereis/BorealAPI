from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class Order(BaseModel):
    user_client: str
    order_value: float
    previous_order: bool


class Brewery(BaseModel):
    id: str
    name: str
    brewery_type: Optional[str]
    street: Optional[str]
    address_2: Optional[str]
    address_3: Optional[str]
    city: Optional[str]
    state: Optional[str]
    county_province: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    longitude: Optional[str]
    latitude: Optional[str]
    phone: Optional[str]
    website_url: Optional[str]
    updated_at: datetime
    created_at: datetime


class Breweries_names(BaseModel):
    names: List[str]
