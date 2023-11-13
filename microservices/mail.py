import smtplib
from email.mime.text import MIMEText
from random import choices

class EmailService:
    def __init__(self, smtp_server, smtp_port, my_email, my_password):
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.__my_email = my_email
        self.__my_password = my_password

    def send_message(self, to_email: str):
        code = self.__generate_code()
        msg = MIMEText(f"Подтверждение учетной записи\nВаш код - {code}")
        msg['Subject'] = 'Подтверждение учетной записи'
        msg['From'] = self.__my_email
        msg['To'] = to_email

        with smtplib.SMTP(self.__smtp_server, self.__smtp_port) as server:
            server.starttls()
            server.login(self.__my_email, self.__my_password)
            server.sendmail(self.__my_email, to_email, msg.as_string())

        return int(code)

    def __generate_code(self):
        verification_code = ''.join(choices('0123456789', k=6))
        return verification_code