#!/bin/python3

from variables import *
from key import *
import requests
from datetime import datetime
import json
from customemail import *

headers = {
    'Accept': 'application/json',
    'authorization': f'Bearer {API_TOKEN}'
}

# Request que pega as duas últimas guerras
url = f'https://api.clashroyale.com/v1/clans/%23{CLAN_TAG}/riverracelog?limit={LIMIT}'
response = requests.get(url, headers=headers)

# Pegando quem ainda tá no clã
url = f'https://api.clashroyale.com/v1/clans/%23{CLAN_TAG}/members?limit={50}'
response_playerNoCla = requests.get(url, headers=headers)

# Nova estrutura de dados unificada
jogadores_analise = {}
datas_guerras = []

if response.status_code == 200 and response_playerNoCla.status_code == 200:
    river_log = response.json()
    players_no_cla = response_playerNoCla.json()

    players_atuais = [player['name'] for player in players_no_cla['items']]
    
    # Iterando sobre as duas últimas guerras
    for i, guerra in enumerate(river_log['items']):
        # Pegando e formatando a data
        data = guerra['createdDate'][:8]
        data = datetime.strptime(data, '%Y%m%d')
        datas_guerras.append(data)
        
        for standing in guerra['standings']:
            # Pegando os dados do clã escolhido pela CLAN_TAG
            if standing['clan']['tag'] == '#' + CLAN_TAG:
                # Cria o dicionario de todos os players e suas pontuacoes
                lista_pontuacao = {participant['name']: participant['fame'] for participant in standing['clan']['participants']}
                
                for player, pontuacao in lista_pontuacao.items():
                    if player in players_atuais:
                        if i == 0:  # Guerra mais recente
                            if player not in jogadores_analise:
                                jogadores_analise[player] = [pontuacao, None, None]
                            else:
                                jogadores_analise[player][0] = pontuacao
                            
                            if pontuacao <= MIN_EXPULSO:
                                jogadores_analise[player][2] = 'expulso'
                            elif MIN_EXPULSO < pontuacao < MIN_PONTOS:
                                jogadores_analise[player][2] = 'blacklist'
                        elif i == 1:  # Penúltima guerra
                            if player in jogadores_analise:
                                jogadores_analise[player][1] = pontuacao
                                if MIN_EXPULSO < pontuacao < MIN_PONTOS and jogadores_analise[player][2] == 'blacklist':
                                    jogadores_analise[player][2] = 'expulso por blacklist'
                            else:
                                jogadores_analise[player] = [None, pontuacao, None]

    data_primeira_guerra, data_segunda_guerra = datas_guerras

    # Removendo jogadores que não têm status definido
    jogadores_analise = {k: v for k, v in jogadores_analise.items() if v[2] is not None}

else:
    print(f'Erro na requisição: {response.status_code}: {response.text}')
    print(f'Erro na requisição de membros: {response_playerNoCla.status_code}: {response_playerNoCla.text}')

# Formatando a data para o e-mail
data_formatada = data_primeira_guerra.strftime('%d/%m/%Y')


# Chamada da função de envio de e-mail
enviarEmail(data_formatada, jogadores_analise)

print("Jogadores analisados:", jogadores_analise)
print("Data primeira guerra:", data_primeira_guerra)
print("Data segunda guerra:", data_segunda_guerra)