from twilio.rest import Client
from dotenv import load_dotenv
import os, sys, json
from nominationParser import parseNominations
from pdfExtractor import extractPdfText

load_dotenv()

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
personal_phone_number = os.getenv("PERSONAL_PHONE_NUMBER")
ngrok_url = os.getenv("NGROK_URL")

if not all([account_sid, auth_token, twilio_phone_number, personal_phone_number]):
    raise ValueError("Missing required environment variables")

assert account_sid is not None
assert auth_token is not None
assert twilio_phone_number is not None
assert personal_phone_number is not None

client = Client(account_sid, auth_token)

if __name__ == "__main__":

    if len(sys.argv) == 2:
        pdfContent = extractPdfText(sys.argv[1])
    else:
        raise ValueError("Wrong number of arguments, 1 needed (pdf)")

    games = parseNominations(pdfContent)

    if not isinstance(games, list):
        raise ValueError("Failed to parse games from PDF")

    if len(games) == 0:
        print("No games found, exiting...")
        sys.exit(0)

    with open("games.json", "w") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)

    VPS_IP = "http://77.237.242.67:8000"

    twiml = f"""<Response>
                    <Say language="pt-PT">{
                        f'Existe 1 jogo sem árbitro' if len(games) == 1 
                        else f'Existem {len(games)} jogos sem árbitro'
                    }</Say>
                    <Redirect method="POST">{VPS_IP}/game/0</Redirect>
                    <Hangup/>
                </Response>"""
    call = client.calls.create(
        to=personal_phone_number,
        from_=twilio_phone_number,
        twiml=twiml
    )

    print(call.sid)
