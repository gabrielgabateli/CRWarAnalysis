import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from key import PASSWORD
from variables import DESTINATARIOS, REMETENTE

def enviarEmail(data_formatada, expulsos: dict, blacklist):

    # Configuração da mensagem
    msg = MIMEMultipart()
    msg['From'] = REMETENTE
    msg['To'] = DESTINATARIOS
    msg['Subject'] = f"CRWarAnalysis {data_formatada}"
    '''
    '''
    mensagem = f"Expulsos (Menos de 400 pontos):\n {'\n '.join(f'{player}: {pontos} pontos' for player, pontos in expulsos.items())}"
    mensagem += '\n\n'
    mensagem += f"Blacklist (Menos de 1800 pontos):\n {'\n '.join(f'{player}: {pontos} pontos' for player, pontos in blacklist.items())}"
    mensagem += '\n\n'
    mensagem += 'https://royaleapi.com/clan/Q0V2YYUL/war/analytics'


    # # Cria as seções formatadas separadamente
    # expulsos = '\n'.join(f'{player}: {pontos} pontos' for player, pontos in expulsos.items())
    # blacklist = '\n'.join(f'{player}: {pontos} pontos' for player, pontos in blacklist.items())

    # # Concatena as seções em uma única mensagem
    # mensagem = (
    # f"Expulsos (Menos de 400 pontos):\n{expulsos}\n"
    # f"--------------------------------------------------------------------\n" 
    # f"Blacklist (Menos de 1800 pontos):\n{blacklist}"
    # )


    # Formatando a mensagem como uma tabela em HTML

    mensagem = """
    <html>
    <head>
    <style>
    table {
      width: 40%;
      border-collapse: collapse;
    }
    @media only screen and (max-width: 600px) {
      table {
      width: 100%;
        }
    }
    th, td {
      border: 1px solid black;
      padding: 8px;
      text-align: center;
    }
    th {
      background-color: #E8E8E8;
    }
    .titulo {
      background-color: #4CAF50;
      color: white;
    }
    .blacklist {
      background-color: #FFA500;
    }
    .expulso {
      background-color: #FF5733;
    }
  </style>
</head>
<body>
  <h2>Relatório de Pontuações</h2>
  <table>
    <tr>
      <th class="titulo">Nome do Jogador</th>
      <th class="titulo">Pontuação última guerra</th>
      <th class="titulo">Pontuação penúltima guerra</th>
      <th class="titulo">Status</th>
    </tr>
    """
    
    # Populando a tabela com expulsos
    i = 0
    for nome, pontos in expulsos.items():
        mensagem += f""" 
            <tr>
            <th>{nome}</th>
            <th>{pontos}</th>
            <th>Pontuação penúltima guerra</th>
            <th class="expulso">Expulso</th>
        </tr>
        """
        i += 1
    mensagem += "</table>"
    mensagem += "<br>"
    mensagem += "<table>"
    mensagem +=  """ 
      <tr>
      <th class="titulo">Nome do Jogador</th>
      <th class="titulo">Pontuação última guerra</th>
      <th class="titulo">Pontuação penúltima guerra</th>
      <th class="titulo">Status</th>
    </tr>
    """
    
    # Populando a tabela com blacklist
    i = 0
    for nome, pontos in blacklist.items():
        mensagem += f""" 
            <tr>
            <th>{nome}</th>
            <th>{pontos}</th>
            <th>Pontuação penúltima guerra</th>
            <th class="blacklist">Blacklist</th>
        </tr>
        """
        i += 1
    mensagem += "</table>"
    

    # Corpo da mensagem
    msg.attach(MIMEText(mensagem, 'html'))

    # Configuração do servidor Gmail
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()

    # Autenticação no Gmail
    servidor.login(REMETENTE, PASSWORD)

    # Envio do email
    servidor.send_message(msg)
    servidor.quit()


