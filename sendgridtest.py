# needs send grid
import os

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

message = Mail(
    from_email="dqpqt8@umsystem.edu",
    to_emails="khai1995pham@gmail.com",
    subject="Hello from SendGrid",
    plain_text_content="This is a test email sent via SendGrid!",
)

try:
    sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(str(e))
