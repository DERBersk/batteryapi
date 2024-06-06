import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Add your email configuration here
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USERNAME = 'ffb.procure@gmail.com'
EMAIL_PASSWORD = 'ffbprosem@20224'

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