import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def enviarEmail(email_enviar: str):
    # informações do servidor
    host = "smtp.gmail.com"
    port = "587"
    user = "elvis.cavalcante.ematerce@gmail.com"
    password = "mzixctzqfrzccuae"

    server = smtplib.SMTP(host=host, port=port)
    server.starttls()
    server.login(user=user, password=password)

    # informações do e-mail
    corpo = f"""
    <p>E-mail automático do <b>KM Gestão</b></p>
    """
    email_msg = MIMEMultipart()
    email_msg['From'] = user
    email_msg['To'] = email_enviar
    email_msg['Subject'] = "Planilha de vendas e custo por entregador"
    email_msg.attach(MIMEText(corpo, 'html'))

    # colocando arquivos anexos
    # 1º arquivo
    arquivo = r'C:\Users\Elvis\PycharmProjects\clickmoto\teste_dados_mapa.xlsx'
    arquivo_aberto = open(arquivo, 'rb')  # read and binary
    nome_do_arquivo = 'Planilha de Vendas do dia'.encode('utf-8').decode('utf-8', "strict")

    att = MIMEBase('application', 'octet-stream')
    att.set_payload(arquivo_aberto.read())
    encoders.encode_base64(att)  # transformando o arquivo em base64

    att.add_header('Content-Disposition', 'attachment', filename=f"{nome_do_arquivo}.xlsx")
    arquivo_aberto.close()
    email_msg.attach(att)

    # 2º arquivo
    arquivo2 = r'C:\Users\Elvis\PycharmProjects\clickmoto\Valor a pagar por entregador.xlsx'
    arquivo_aberto2 = open(arquivo2, 'rb')  # read and binary
    nome_do_arquivo2 = 'Planilha de Custos por Entregador'.encode('utf-8').decode('utf-8', "strict")

    att2 = MIMEBase('application', 'octet-stream')
    att2.set_payload(arquivo_aberto2.read())
    encoders.encode_base64(att2)  # transformando o arquivo em base64

    att2.add_header('Content-Disposition', 'attachment', filename=f"{nome_do_arquivo2}.xlsx")
    arquivo_aberto2.close()
    email_msg.attach(att2)

    # enviar o e-mail
    server.sendmail(from_addr=email_msg['From'], to_addrs=email_msg['To'], msg=email_msg.as_string().encode('utf-8'))
    server.quit()
    # print("E-mail enviado com sucesso!")


# # enviando e-mails para uma lista de e-mails
# emails = ['elvispcce@gmail.com']
# for i in emails:
#     enviarEmail(i)
