from typing import Optional, List
from pydantic import BaseModel


class ReaderInfo(BaseModel):
    registration_code: str
    label: str
    location: str


class PaymentIntentInfo(BaseModel):
    payment_method_types: Optional[List[str]] = ['card_present']
    amount: int
    currency: Optional[str] = 'gbp'
    capture_method: Optional[str] = 'manual'
    description: Optional[str] = 'Test Payment'


