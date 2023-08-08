from typing import Optional, List
from fastapi import Form
from pydantic import BaseModel

def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

@form_body
class ReaderInfo(BaseModel):
    registration_code: str
    label: str
    location: str

@form_body
class PaymentIntentInfo(BaseModel):
    payment_method_types: Optional[List[str]] = ['card_present']
    amount: int
    currency: Optional[str] = 'gbp'
    capture_method: Optional[str] = 'manual'
    description: Optional[str] = 'Test Payment'


