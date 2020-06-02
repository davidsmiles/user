import os

from requests import Response
from sendgrid import SendGridAPIClient, Mail


class SendmailException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Sendmail:
    @classmethod
    def send_email(cls, email: str, subject: str, text: str) -> Response:
        message = Mail(
            from_email='ugberodavid@gmail.com',
            to_emails=email,
            subject=subject,
            html_content=text)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
        except Exception as e:
            print(e.message)

        return response
