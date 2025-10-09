from twilio.rest import Client
from dotenv import load_dotenv
import os, sys
from nominationParser import parse_nominations
from pdfExtractor import extract_pdf_text

def pretty_print_games(games):
    return_text = ""
    introduction = "Existe 1 jogo sem nomeação.\n" if len(games) == 1 else "Existem jogos sem nomeação.\n"
    return_text += introduction

    ordinal_values = ["Primeiro jogo: ", "Segundo jogo: ", "Terceiro jogo: ", "Quarto jogo: ", "Quinto jogo: ",
                      "Sexto jogo: ", "Sétimo jogo: ", "Oitavo jogo: ", "Nono jogo: ", "Décimo jogo: "]
    
    for game_number in range(len(games)):
        if len(games) != 1:
            return_text += ordinal_values[game_number]

        return_text += (f'{games[game_number]["data"]} '
                   f'{games[game_number]["hora"]} '
                   f'{games[game_number]["escalão"]} '
                   f'{games[game_number]["equipas_e_pavilhão"]}\n')

    return return_text


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

if len(sys.argv) == 2:
    pdfContent = extract_pdf_text(sys.argv[1])
else:
    raise ValueError("Wrong number of arguments, 1 needed (pdf)")

games = parse_nominations(pdfContent)

twiml = f"""<Response>
                <Gather numDigits="1" action="{ngrok_url}/manage-call" method="POST">
                    <Say language="pt-PT">Funciona</Say>
                </Gather>    
            </Response>"""
call = client.calls.create(
    to=personal_phone_number,
    from_=twilio_phone_number,
    twiml=twiml
)

print(call.sid)

# print(pretty_print_games(games))