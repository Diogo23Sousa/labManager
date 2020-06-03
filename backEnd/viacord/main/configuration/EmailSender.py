from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint
import smtplib, ssl

# BLUEPRINT (project_configuration)
email_sender = Blueprint('email_sender', __name__, template_folder='templates')


class EmailSender:
    def __init__(self):
        self = self

    @staticmethod
    def sendEmailTest():
        subject = "ViaCord - Processed Samples"
        body = "This email contains an excel file with the processed sample data"
        sender_email = "dioguinhosousinha23@gmail.com"
        receiver_email = "diogo.sousa23@outlook.com"
        password = input("Type your password and press enter:")

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)


    @staticmethod
    def sendEmail(emailToSend, message):
        subject = "ViaCord - Processed Samples"
        body = message
        sender_email = "dioguinhosousinha23@gmail.com"
        receiver_email = emailToSend
        password = input("Type your password and press enter:")

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)