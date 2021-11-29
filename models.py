from logs.customlogger import logger
import re
from datetime import datetime
from pydantic import BaseModel, validator
from typing import List, Optional

RE_NAMES = "[A-Za-z]{2,30}"

RE_BREWERY_NAMES = "[A-Za-z0-9. -]{2,50}"

class Order(BaseModel):
    user_client: str
    order_value: float
    previous_order: bool

    @validator('user_client')
    def is_user_client_valid(cls, user_client):
        if re.fullmatch(RE_NAMES, user_client) is None:
            raise ValueError("user/client invalid")
        return user_client

    @validator('order_value')
    def value_is_positive(cls, order_value):
        if order_value < 0:
            logger.error('negative order_value')
            raise ValueError('negative order_value')
        return order_value

    @validator('previous_order')
    def is_bolean(cls, previous_order):
        if isinstance(previous_order, bool):
            return previous_order
        raise ValueError("value isn't boolean")


class Brewery(BaseModel):
    id: Optional[str]
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
    updated_at: Optional[datetime]
    created_at: Optional[datetime]

    @validator('name')
    def is_string(cls, name):
        if isinstance(name, str):
            return name
        raise ValueError('not a string')

    @validator('name')
    def is_name_valid(cls, name):
        if re.fullmatch(RE_BREWERY_NAMES, name) is None:
            raise ValueError("name invalid")
        return name

class Breweries_names(BaseModel):
    names: List[str]

    @validator('names')
    def is_string(cls, names):
        if isinstance(names, List):
            return names
        raise ValueError('not a List')
