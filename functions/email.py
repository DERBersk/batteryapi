import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

with open('config.json', 'r') as file:
    config = json.load(file)

# Add your email configuration here
EMAIL_HOST = config['EMAIL_HOST']
EMAIL_PORT = config['EMAIL_PORT']
EMAIL_USERNAME = config['EMAIL_USERNAME']
EMAIL_PASSWORD = config['EMAIL_PASSWORD']

def send_email(email, subject, html_content):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USERNAME
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USERNAME, email, msg.as_string())
    server.quit()