import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from key import PASSWORD
from variables import DESTINATARIOS, REMETENTE

def enviarEmail(data_formatada, expulsos, blacklist):

    # Configuração da mensagem
    msg = MIMEMultipart()
    msg['From'] = REMETENTE
    msg['To'] = DESTINATARIOS
    msg['Subject'] = f"CRWarAnalysis {data_formatada}"
    '''
    mensagem = f"Expulsos (Menos de 400 pontos):\n {'\n '.join(f'{player}: {pontos} pontos' for player, pontos in expulsos.items())}"
    mensagem += '\n\n'
    mensagem += f"Blacklist (Menos de 1800 pontos):\n {'\n '.join(f'{player}: {pontos} pontos' for player, pontos in blacklist.items())}"
    mensagem += '\n\n'
    mensagem += 'https://royaleapi.com/clan/Q0V2YYUL/war/analytics'
    '''

    # Cria as seções formatadas separadamente
    expulsos = '\n'.join(f'{player}: {pontos} pontos' for player, pontos in expulsos.items())
    blacklist = '\n'.join(f'{player}: {pontos} pontos' for player, pontos in blacklist.items())

    # Concatena as seções em uma única mensagem
    mensagem = (
    f"Expulsos (Menos de 400 pontos):\n{expulsos}\n"
    f"---------------------------------------------------------\n"
    f"Blacklist (Menos de 1800 pontos):\n{blacklist}"
    )


    # Corpo da mensagem
    msg.attach(MIMEText(mensagem, 'plain'))

    # Configuração do servidor Gmail
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()

    # Autenticação no Gmail
    servidor.login(REMETENTE, PASSWORD)

    # Envio do email
    servidor.send_message(msg)
    servidor.quit()

