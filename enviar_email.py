from getpass import getpass
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Servidor del correo
smtp_server = 'smtp-mail.outlook.com'
port = 587

#Ingreso de correos y contraseña
print('Datos del correo ha enviar\n')
sender_email = input('Ingrese su correo: ')
password = getpass('Ingrese su contraseña: ')
receiver_email = input('Ingrese el correo del destinatario: ')

#Ingreso de datos del correo
subject = input('Ingrese el asunto del correo: ')
autor = input('Ingrese el nombre del autor del correo (nombre y apellido): ')
message = input('Ingrese el mensaje del texto: ') + f'\n\nAtte:\n{autor}'

#Ingreso de archivo adjunto
filename = input('Ingrese la url del archivo (deje el espacio vacio si no adjuntará archivo): ')
only_filename = os.path.basename(filename)

#Creación del mensaje
msg = MIMEMultipart()
msg.attach(MIMEText(message, 'plain'))

msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

#Adjuntar archivo, el if es porque si no ingresas la url se salta este paso
if only_filename:
    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header('Content-Disposition', f'attachment; filename= {only_filename}')

    msg.attach(part)

text = msg.as_string()

#Envío del correo
with smtplib.SMTP(smtp_server, port) as server:
    print('Conectando al servidor...')
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()
    print('Correo enviado exitosamente')
