from fastapi import Depends, FastAPI, Form, Request  
from fastapi.responses import JSONResponse, FileResponse  
from fastapi.middleware.cors import CORSMiddleware  
from dotenv import load_dotenv
import stripe  
import os

from models import PaymentIntentInfo, ReaderInfo  

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
async def register_reader(reader_info: ReaderInfo = Depends(ReaderInfo)):  
    try:  
        reader = stripe.terminal.Reader.create(  
            **reader_info 
        )  
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
async def create_payment_intent(payment_info: PaymentIntentInfo = Depends(PaymentIntentInfo)):  
    try:  
        payment_intent = stripe.PaymentIntent.create(  
            **payment_info
        )  
        return JSONResponse({  
            "intent": payment_intent.id,  
            "secret": payment_intent.client_secret  
        })  
    except Exception as e:  
        # handle error  
        pass  
  
@app.post("/capture_payment_intent")  
async def capture_payment_intent(request: Request):  
    # Implementation here  
    pass  
  
@app.post("/cancel_payment_intent")  
async def cancel_payment_intent(request: Request):  
    # Implementation here  
    pass  
  
@app.post("/create_setup_intent")  
async def create_setup_intent(request: Request):  
    # Implementation here  
    pass  
  
@app.post("/attach_payment_method_to_customer")  
async def attach_payment_method_to_customer(request: Request):  
    # Implementation here  
    pass  