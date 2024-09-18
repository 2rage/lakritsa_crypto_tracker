import smtplib
from email.message import EmailMessage


def send_email(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'no-reply@example.com'
    msg['To'] = 'recipient@example.com'

    
    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)
