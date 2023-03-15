from workers import celery
from models import *
import csv
from werkzeug.utils import secure_filename
import smtplib
from email import encoders
# from email.utils import COMMASPACE
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'your-email-address@gmail.com'
MAIL_PASSWORD = None


@celery.task
def just_say_hello(name):
    print("INSTIDE TASK")
    print(f"Hello {name}")


@celery.task
def send_email(email_addres):
    msg = MIMEMultipart()
    msg['From'] = f'Ashraf khan {MAIL_USERNAME}'
    msg['To'] = email_addres
    msg['Subject'] = "Exported blog data"
    body = '''Hello,
            this your whole blog data.'''
    msg.attach(MIMEText(body, 'plain'))
    # create_csv(email=email_addres)
    # filename = secure_filename('output.csv')
    # with open(file=filename) as attachment:
    #     part = MIMEBase('application', 'octet-stream')
    #     part.set_payload(attachment.read())
    #     encoders.encode_base64(part)
    #     part.add_header('Content-Disposition',
    #                     f"attachment; filename= {filename.split('/')[-1]}")
    #     msg.attach(part)
    # attachment.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        # server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, email_addres, msg.as_string())
    return print({'message': 'Email sent successfully!'})


def create_csv(email):
    user = User.query.filter(User.email == email).one()
    blogs = user.blogs
    data = [{"Title": blog.title, "Description": blog.description, "Timestamp": blog.timestamp}
            for blog in blogs
            ]

    # Define fieldnames for CSV header
    fieldnames = ['Title', 'Description', 'Timestamp']

    # Open CSV file for writing
    with open('output.csv', mode='w', newline='') as csv_file:
        # Create CSV writer object
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header row
        writer.writeheader()

        # Write data rows
        for row in data:
            writer.writerow(row)
