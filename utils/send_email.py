import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to send email
def send_email(to_email, subject, message):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "mekastans@gmail.com"
    app_password = os.getenv("EMAIL_PASSWORD")

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login to the SMTP server
    server.login(sender_email, app_password)

    # Send the email
    server.sendmail(sender_email, to_email, msg.as_string())

    print(f"Email has been sent to {to_email}.")
    # Quit the SMTP server
    server.quit()
