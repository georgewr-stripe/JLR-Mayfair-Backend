from typing import List, Optional, Type
from fastapi import Form
import inspect

from pydantic import BaseModel
from pydantic.fields import FieldInfo

DESCRIPTION = 'JLR L460 Range Rover Reservation'


def as_form(cls: Type[BaseModel]):
    new_parameters = []

    for field_name, model_field in cls.__fields__.items():
        model_field: FieldInfo  # type: ignore
        new_parameters.append(
             inspect.Parameter(
                 field_name,
                 inspect.Parameter.POSITIONAL_ONLY,
                 default=Form(...) if model_field.is_required() else Form(model_field.default),
                 annotation=model_field.annotation,
             )
         )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls

@as_form
class ReaderInfo(BaseModel):
    registration_code: str
    label: str
    location: str

@as_form
class PaymentIntentInfo(BaseModel):
    amount: int
    customer: str
    currency: Optional[str] = 'gbp'
    payment_method_types: Optional[List[str]] = ['card_present']
    capture_method: Optional[str] = 'manual'
    description: Optional[str] = DESCRIPTION


@as_form
class CaptureCancelPaymentIntentInfo(BaseModel):
    payment_intent_id: str


@as_form
class CreateSetupIntentInfo(BaseModel):
    payment_method_types: Optional[List[str]] = ['card_present']
    customer: Optional[str]
    description: Optional[str] = DESCRIPTION
    on_behalf_of: Optional[str]


@as_form
class CreateCustomerInfo(BaseModel):
    name: str
    email: str
    phone: str