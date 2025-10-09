# api.py
from fastapi import FastAPI, Form
from fastapi.responses import Response

app = FastAPI()

@app.get("/health")
def health():
    return "API active."

@app.post("/manage-call")
def manage_call(Digits: str = Form(...)):
    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="pt-PT">Recebi o teu input que é o número {Digits}. Obrigado!</Say>
    <Hangup/>
</Response>"""
    return Response(content=twiml_response, media_type="application/xml")
