from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import stripe
import os

from models import (
    CreateCustomerInfo,
    PaymentIntentInfo,
    ReaderInfo,
    CaptureCancelPaymentIntentInfo,
    CreateSetupIntentInfo,
)

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")


@app.post("/register_reader")
async def register_reader(reader_info: ReaderInfo = Depends(ReaderInfo.as_form)):
    try:
        reader = stripe.terminal.Reader.create(**reader_info)
        return JSONResponse(reader)
    except Exception as e:
        # handle error
        pass


@app.post("/connection_token")
async def connection_token():
    try:
        token = stripe.terminal.ConnectionToken.create()
        return JSONResponse({"secret": token.secret})
    except Exception as e:
        # handle error
        pass


@app.post("/create_payment_intent")
async def create_payment_intent(
    payment_info: PaymentIntentInfo = Depends(PaymentIntentInfo.as_form),
):
    try:
        payment_intent = stripe.PaymentIntent.create(**payment_info.model_dump())
        return JSONResponse(
            {"intent": payment_intent.id, "secret": payment_intent.client_secret}
        )
    except Exception as e:
        # handle error
        print(e)
        pass


@app.post("/capture_payment_intent")
async def capture_payment_intent(
    data: CaptureCancelPaymentIntentInfo = Depends(
        CaptureCancelPaymentIntentInfo.as_form
    ),
):
    stripe.PaymentIntent.retrieve(data.payment_intent_id).capture()


@app.post("/cancel_payment_intent")
async def cancel_payment_intent(
    data: CaptureCancelPaymentIntentInfo = Depends(
        CaptureCancelPaymentIntentInfo.as_form
    ),
):
    stripe.PaymentIntent.retrieve(data.payment_intent_id).cancel()


@app.post("/create_setup_intent")
async def create_setup_intent(
    setup_info: CreateSetupIntentInfo = Depends(CreateSetupIntentInfo.as_form),
):
    try:
        setup_intent = stripe.SetupAttempt.create(**setup_info.model_dump())
        return JSONResponse(
            {"intent": setup_intent.id, "secret": setup_intent.client_secret}
        )
    except Exception as e:
        # handle error
        print(e)
        pass


@app.post("/attach_payment_method_to_customer")
async def attach_payment_method_to_customer(request: Request):
    # Implementation here
    pass


@app.post("/create_customer")
async def create_customer(
    customer_info: CreateCustomerInfo = Depends(CreateCustomerInfo.as_form),
):
    # try to find an existing customer
    customers = stripe.Customer.search(query="email:'{}'".format(customer_info.email))
    if len(customers.data) > 0:
        customer_id = customers.data[0].id
    else:
        customer_id = stripe.Customer.create(**customer_info.model_dump()).id
    return JSONResponse({"customer_id": customer_id})
