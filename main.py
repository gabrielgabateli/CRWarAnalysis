#!/bin/python3

from variables import *
from key import *
import requests
from datetime import datetime
import json
from customemail import *

url = f'https://api.clashroyale.com/v1/clans/%23{CLAN_TAG}/riverracelog?limit={LIMIT}'

headers = {
    'Accept': 'application/json',
    'authorization': f'Bearer {API_TOKEN}'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    river_log = response.json()
    
    # Pegando e formatando a data
    for race in river_log['items']:  
        data = race['createdDate'][:8]
        data = datetime.strptime(data, '%Y%m%d')
        data_formatada = data.strftime('%d/%m/%Y')
        print(f'Data da guerra: {data}')
        
        for standing in race['standings']:
            if standing['clan']['tag'] == '#' + CLAN_TAG:  # Pegando os dados do clã escolhido pela CLAN_TAG
                
                lista_pontuacao = {participant['name']: participant['fame'] for participant in standing['clan']['participants']} # Cria o dicionario dos players e suas pontuacoes    
                lista_pontuacao = dict(sorted(lista_pontuacao.items(), key=lambda item: item[1], reverse=True)) # Ordena da maior para menor pontuação
                
                expulsos = {}
                blacklist = {}
                for player in lista_pontuacao:
                    if lista_pontuacao[player] <= MIN_EXPULSO:
                        expulsos[player] = lista_pontuacao[player]
                    elif MIN_EXPULSO < lista_pontuacao[player] < MIN_PONTOS:
                        blacklist[player] = lista_pontuacao[player]
                
                enviarEmail(data_formatada, expulsos, blacklist)

    
else:
    print(f'Erro: {response.status_code}: {response.text}')
