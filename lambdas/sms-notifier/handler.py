import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sms_notifier(event, context):

    # for debugging the state machine
    print(event)
    
    destination_email = event['email']
    object_link = event['audio_link']

    username = "lisingo.mailer@gmail.com"
    password = "lisingo1!"
    subject = "Your Lisingo MP3 is ready."
    message = f'''Your lisingo data is finished. Please click the link to download!
    
    {object_link}
    
    Thank you for using Lisingo!
    '''
    
    # Start email server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)

    # Create and send email
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = destination_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    body = msg.as_string()
    server.sendmail(username, destination_email, body)


    response = {
        "statusCode": 200
    }

    return response
