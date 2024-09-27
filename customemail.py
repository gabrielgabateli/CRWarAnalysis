import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from key import PASSWORD
from variables import DESTINATARIOS, REMETENTE

def enviarEmail(data_formatada, jogadores_analise):
    # Configuração da mensagem
    msg = MIMEMultipart()
    msg['From'] = REMETENTE
    msg['To'] = DESTINATARIOS
    msg['Subject'] = f"CRWarAnalysis {data_formatada}"

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

    # Ordenando jogadores por status
    ordem_status = {'expulso': 1, 'blacklist': 2, 'expulso por blacklist': 3}
    jogadores_ordenados = sorted(jogadores_analise.items(), key=lambda x: ordem_status.get(x[1][2], 4))

    # Populando a tabela com os jogadores ordenados
    for nome, (pontos_recentes, pontos_antigos, status) in jogadores_ordenados:
        status_class = "blacklist" if status == "blacklist" else "expulso"
        mensagem += f"""
        <tr>
            <th>{nome}</th>
            <th>{pontos_recentes if pontos_recentes is not None else 'N/A'}</th>
            <th>{pontos_antigos if pontos_antigos is not None else 'N/A'}</th>
            <th class="{status_class}">{status.capitalize()}</th>
        </tr>
        """

    mensagem += "</table><br>"
    mensagem += 'https://royaleapi.com/clan/Q0V2YYUL/war/analytics'

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