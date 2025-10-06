from twilio.rest import Client
from dotenv import load_dotenv
import os
from nominationParser import parse_nominations
from pdfExtractor import allText as pdfContent

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
auth_token = os.getenv("AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
personal_phone_number = os.getenv("PERSONAL_PHONE_NUMBER")

client = Client(account_sid, auth_token)

games = parse_nominations(pdfContent)

call = client.calls.create(
    to=personal_phone_number,
    from_=twilio_phone_number,
    twiml=f'<Response><Say language="pt-PT">{pretty_print_games(games)}</Say></Response>'
)

print(call.sid)