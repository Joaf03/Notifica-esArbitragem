from enum import Enum
import re

class Dates(Enum):
    SEGUNDA_FEIRA = "segunda-feira"
    TERCA_FEIRA = "terça-feira"
    QUARTA_FEIRA = "quarta-feira"
    QUINTA_FEIRA = "quinta-feira"
    SEXTA_FEIRA = "sexta-feira"
    SABADO = "sábado"
    DOMINGO = "domingo"


def parse_nominations(info):
    no_referee_games = []
    data_atual = "Data desconhecida"

    for line in info.split('\n'):
        line = line.strip()

        if "Associação de Patinagem do Porto" in line or "Conselho de Arbitragem" in line or "N O M E A Ç Õ E S" in line or "Tipo Jogo Hora" in line or "Página" in line:
            continue
        
        if any(date.value in line for date in Dates):
            data_atual = line
            continue

        match = re.search(r'(SUB\d{2})\s(\d{1,3})\s(\d{1,2}):(\d{2})\s(.*(?=\d{1,2}))(\d{1,2})(.*)', line)

        if match:
            escalão = match.group(1).strip()
            hora = f'{match.group(3)}:{match.group(4)}'
            equipas_e_pavilhão = match.group(5).strip()
            árbitros = match.group(7).strip()

            build_no_referee_games(data_atual, escalão, hora, equipas_e_pavilhão, árbitros, no_referee_games)
        
        if "SUB" not in line or not match:
            return ValueError("Error while parsing PDF")
    

    return no_referee_games
        

def build_no_referee_games(data_atual, escalão, hora, equipas_e_pavilhão, árbitros, no_referee_games):

    if not árbitros:
            game = {
                "data": data_atual,
                "hora": hora,
                "escalão": escalão,
                "equipas_e_pavilhão": equipas_e_pavilhão,
                "árbitros": árbitros
            }

            no_referee_games.append(game)

    return no_referee_games

# print(parse_nominations(pdfContent))