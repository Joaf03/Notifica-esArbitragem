from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
personal_phone_number = os.getenv("PERSONAL_PHONE_NUMBER")

client = Client(account_sid, auth_token)

call = client.calls.create(
    to=personal_phone_number,
    from_=twilio_phone_number,
    twiml="<Response><Say>Olá! Isto é um teste do Twilio. A tua chamada está a funcionar.</Say></Response>"
)

print(call.sid)