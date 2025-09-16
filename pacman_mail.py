import os
import subprocess

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

x = 0
for x in range(10000000):
    x += 1

output = "Program Finished"

# build email
message = Mail(
    from_email="dqpqt8@umsystem.edu",  # must be verified in SendGrid
    to_emails="dqpqt8@umsystem.edu",  # send to yourself
    subject="number",
    plain_text_content=output,
)

try:
    sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])
    response = sg.send(message)
    print("Email sent!", response.status_code)
except Exception as e:
    print("Error sending email:", e)
