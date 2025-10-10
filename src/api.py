from fastapi import FastAPI, Form
from fastapi.responses import Response
import requests, os, json

ordinal_values = ["Primeiro jogo: ", "Segundo jogo: ", "Terceiro jogo: ", "Quarto jogo: ", "Quinto jogo: ",
                      "Sexto jogo: ", "Sétimo jogo: ", "Oitavo jogo: ", "Nono jogo: ", "Décimo jogo: "]

app = FastAPI()

def load_games():
    if not os.path.exists("games.json"):
        return []
    with open("games.json", "r") as f:
        return json.load(f)

@app.get("/health")
def health():
    return "API active."

@app.post("/game/{index}")
def handle_game(index: int):    
    games = load_games()

    if not isinstance(games, list):
        raise ValueError("Failed importing games from twilioTest.py")
    
    if index >= len(games):
        twiml = f"""<Response>
                <Say language="pt-PT"> Não há mais jogos sem árbitro. Adeus. </Say>
                <Hangup/>
            </Response>"""
        return Response(twiml, media_type="application/xml")
    
    game = games[index]

    twiml = f"""<Response>
                <Say language="pt-PT"> {ordinal_values[index]} </Say>
                <Say language="pt-PT"> {game["data"]} </Say>
                <Say language="pt-PT"> às {game["hora"]} </Say>
                <Say language="pt-PT"> escalão {game["escalão"]} </Say>
                <Say language="pt-PT"> {game["equipas_e_pavilhão"]} </Say>

                <Gather numDigits="1" action="/response/{index}" method="POST"> </Gather>
            </Response>"""
    
    return Response(twiml, media_type="application/xml")

@app.post("/response/{index}")
def handle_response(index: int, Digits: str = Form(...)):
    games = load_games()

    if not isinstance(games, list):
        raise ValueError("Failed importing games from twilioTest.py")
    print(Digits)
    if Digits == "0":
        message = "Jogo rejeitado."
        new_index = index+1
    
    elif Digits == "1":
        requests.post("http://localhost:3000/send-message", json = {
            "game": games[index]
        })

        message = "Jogo aceite."
        new_index = index+1
        
    else:
        message = "Entrada inválida. A repetir..."
        new_index = index
        
    twiml = f"""<Response>
                <Say language="pt-PT"> {message} </Say>
                <Redirect method="POST"> /game/{new_index}</Redirect>
            </Response>"""

    
    return Response(twiml, media_type="application/xml")
