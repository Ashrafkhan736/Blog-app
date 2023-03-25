from workers import celery
from celery.schedules import crontab
from models import *
import csv
from werkzeug.utils import secure_filename
import smtplib
from email import encoders
import os
# from email.utils import COMMASPACE
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from dateutil.relativedelta import relativedelta
from weasyprint import HTML

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
def daily_reminder():
    users: list[User] = User.query.all()
    current_time = datetime.datetime.now()
    for user in users:
        if (current_time - user.timestamp) >= datetime.timedelta(hours=24):
            print("Given datetime is 24 hours old or more.")
            with open("static/template/daily.html", "r") as fh:
                template = Template(fh.read())
            send_email(email_addres=user.email,
                       subject="Daily reminder",
                       body=template.render(name=user.user_name))

        else:
            print("Given datetime is less than 24 hours old.")
    return 'sucess'


@celery.task
def export_job(user_name: str, email: str):
    filepath = create_csv(email)
    with open('static/template/export_data.html', 'r') as fh:
        template = Template(fh.read())
    send_email(email_addres=email,
               subject="Your exported blog data",
               body=template.render(name=user_name),
               attachment=filepath)
    return 'sucess'


@celery.task
def monthly_report():
    users: list[User] = User.query.all()
    now = datetime.datetime.now()
    one_month_ago = now - relativedelta(months=1)
    for user in users:
        blogs = [blog for blog in user.blogs if blog.timestamp >= one_month_ago]
        following = Follow.query.filter(
            Follow.follower == user.user_name).count()  # persons that user follow
        followers = Follow.query.filter(
            Follow.following == user.user_name).count()  # persons who follow user

        with open('static/template/monthly_report.html', "r") as fh:
            body_template = Template(fh.read())

        with open("static/template/report_pdf.html", "r") as fh:
            pdf_template = Template(fh.read())

        pdf_report = HTML(string=pdf_template.render(
            user=user,
            followers=followers,
            following=following,
            blogs=blogs,
            month=now.strftime('%B %Y'),
        ))
        filepath = f'static/monthly_reports/{user.user_name}_{now}.pdf'
        pdf_report.write_pdf(target=filepath)
        print("sending email\n\n\n")
        send_email(email_addres=user.email,
                   subject="Monthly Report",
                   body=body_template.render(
                       name=user.user_name, num_blogs=len(blogs), num_followers=followers),
                   attachment=filepath)
        print("sent email\n\n\n")
    return 'sucess'


def create_csv(email):
    user = User.query.filter(User.email == email).one()
    blogs = user.blogs
    data = [{"Title": blog.title, "Description": blog.description, "Timestamp": blog.timestamp}
            for blog in blogs
            ]
    # Define fieldnames for CSV header
    fieldnames = ['Title', 'Description', 'Timestamp']
    filepath = f'static/{email}.csv'
    with open(filepath, mode='w', newline='') as csv_file:
        # Create CSV writer object
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
    return filepath


def send_email(email_addres, subject, body, attachment=None):
    msg = MIMEMultipart()
    msg['From'] = f'Ashraf khan {MAIL_USERNAME}'
    msg['To'] = email_addres
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    if attachment:
        with open(file=attachment, mode='rb') as fh:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(fh.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            f"attachment; filename= {attachment.split('/')[-1]}")
            msg.attach(part)
        print(f"Removing {attachment} file from server")
        os.remove(attachment)
    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        # server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, email_addres, msg.as_string())
    return print('Email sent successfully!')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(10.0,
    #                          daily_reminder.s(), name='every 10 senconds daily remainder')
    # sender.add_periodic_task(30.0,
    #                          monthly_report.s(), name='every 10 senconds monthly reports')
    sender.add_periodic_task(crontab(minute=0, hour=20),
                             daily_reminder.s(), name='daily_reminder')
    sender.add_periodic_task(crontab(
        0, 0, day_of_month='1', month_of_year='1-12'), monthly_report.s(), name='monthly_report')
    