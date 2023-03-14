import smtplib
from email import encoders
from email.utils import COMMASPACE
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from celery import Celery
from flask import Flask
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from flask import Flask, request, jsonify
import requests
import json
import os
QUERY_URL = "https://api.openai.com/v1/images/generations"


def generate_image(prompt, model, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "prompt": prompt,
        "num_images": 1,
        "size": "1024x1024",
        "response_format": "url"
    }
    resp = requests.post(QUERY_URL, headers=headers, data=json.dumps(data))
    if resp.status_code != 200:
        raise ValueError("Failed to generate image")
    response_text = json.loads(resp.text)
    return response_text['data'][0]['url']


response = requests.get("https://api.dicebear.com/5.x/adventurer/svg")
print(response.content)

# # DALL-E API endpoint
# url = "https://api.openai.com/v1/images/generations"

# # API key for authentication
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Bearer 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"
# }

# # Request payload with the text prompt
# data = {
#     "model": "image-alpha-001",
#     "prompt": "generate a picture of a dog",
#     "num_images": 1,
#     "size": "1024x1024",
#     "response_format": "url"
# }

# # Make the API request
# response = requests.post(url, headers=headers, data=json.dumps(data))

# # Check if the request was successful
# if response.status_code == 200:
#     # Get the image URL from the response
#     image_url = response.json()["data"][0]["url"]

#     # Download the image and save it to a file
#     image_response = requests.get(image_url)
#     with open("dog_image.jpg", "wb") as f:
#         f.write(image_response.content)

# else:
#     # Handle the error
#     print("Failed to generate image:", response.text)


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'your-email-address@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = (
    'Your Name', 'your-email-address@gmail.com')
app.config['UPLOAD_FOLDER'] = '/path/to/uploads'

mail = Mail(app)


@app.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.form['recipient']
    subject = request.form['subject']
    body = request.form['body']
    attachment = request.files['attachment']
    filename = secure_filename(attachment.filename)
    attachment.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    with app.app_context():
        message = Message(subject=subject, recipients=[recipient], body=body)
        message.attach(filename, attachment.read())
        mail.send(message)
    return jsonify({'message': 'Email sent successfully!'})


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def send_email(recipient, subject, body, attachment):
    # same function as before
    pass


@app.route('/send_email', methods=['POST'])
def send_email_route():
    recipient = request.form['recipient']
    subject = request.form['subject']
    body = request.form['body']
    attachment = request.files['attachment']
    filename = secure_filename(attachment.filename)
    attachment.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    send_email.delay(recipient, subject, body, attachment)
    return jsonify({'message': 'Email will be sent soon!'})


# Define SMTP server and login credentials
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'your-email-address@gmail.com'
smtp_password = 'your-email-password'

# Define message details
sender = 'Your Name <your-email-address@gmail.com>'
recipients = ['recipient1@example.com', 'recipient2@example.com']
subject = 'Test email with attachment'
body = 'This is a test email sent using smtplib in Python.'

# Create message object
msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = COMMASPACE.join(recipients)
msg['Subject'] = subject

# Attach body text
msg.attach(MIMEText(body, 'plain'))

# Attach file as attachment
filename = 'path/to/file.pdf'
with open(filename, 'rb') as attachment:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    f"attachment; filename= {filename.split('/')[-1]}")
    msg.attach(part)

# Connect to SMTP server and login
smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
smtp_conn.ehlo()
smtp_conn.starttls()
smtp_conn.login(smtp_username, smtp_password)

# Send message
smtp_conn.sendmail(sender, recipients, msg.as_string())

# Disconnect from SMTP server
smtp_conn.quit()
