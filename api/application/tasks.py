from celery.schedules import crontab
from application.workers import celery
from datetime import datetime
from flask import current_app as app

from jinja2 import Template
from weasyprint import HTML

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import pandas as pd

from application.models import List, User, Card
from flask_security import current_user


SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = "8081"
SENDER_ADDRESS = "email@me.com"
SENDER_PASSWORD = ""

# WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAv1pcSfo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=eyOFtDJ6Li_OdVmI-D8tGieYQCteoyiNksx2rpqCUS4%3D"

print("crontab ", crontab)


def data_for_monthly_report(current_user_id):

    lists = List.query.filter_by(user_id=current_user_id).all()

    month = datetime.now().strftime("%B")
    total_num_of_lists = len(lists)
    no_of_cards_created = 0
    no_of_cards_completed = 0
    no_of_cards_pending = 0
    no_of_cards_past_deadline = 0

    all_lists_data = []

    for list in lists:

        list_wise_data = {
            "list_id": list.id,
            "list_title": list.title,
            "no_of_cards_created": 0,
            "no_of_cards_completed": 0,
            "no_of_cards_pending": 0,
            "no_of_cards_past_deadline": 0,
            "pending_width": 0,
            "completed_width": 0
        }

        for card in list.cards:
            if card.created_at.month == datetime.today().month:
                no_of_cards_created += 1
                list_wise_data["no_of_cards_created"] += 1

                if card.completed == 1:
                    no_of_cards_completed += 1
                    list_wise_data["no_of_cards_completed"] += 1
                else:
                    no_of_cards_pending += 1
                    list_wise_data["no_of_cards_pending"] += 1
                    if card.deadline.date() < datetime.today().date():
                        no_of_cards_past_deadline += 1
                        list_wise_data["no_of_cards_past_deadline"] += 1

        if list_wise_data['no_of_cards_created'] == 0:

            list_wise_data["pending_width"] = 0

            list_wise_data["completed_width"] = 0

        else:
            list_wise_data["pending_width"] = 100 * \
                list_wise_data["no_of_cards_pending"] / \
                list_wise_data["no_of_cards_created"]

            list_wise_data["completed_width"] = 100 * \
                list_wise_data["no_of_cards_completed"] / \
                list_wise_data["no_of_cards_created"]

        all_lists_data.append(list_wise_data)

    data = {
        "no_of_cards_created": no_of_cards_created,
        "no_of_cards_completed": no_of_cards_completed,
        "no_of_cards_pending": no_of_cards_pending,
        "no_of_cards_past_deadline": no_of_cards_past_deadline,
        "all_lists": all_lists_data,
        "month": month,
        "total_num_of_lists": total_num_of_lists,
    }

    return data


def data_for_daily_reminder(current_user_id):

    lists = List.query.filter_by(user_id=current_user_id).all()

    no_of_pending_tasks_for_the_day = 0

    for list in lists:
        for card in list.cards:
            if card.deadline.date() == datetime.today().date() and card.completed == 0:
                no_of_pending_tasks_for_the_day += 1

    return no_of_pending_tasks_for_the_day


def send_email(to_address, subject, message, attachment_file=""):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    if attachment_file != "":

        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition", f"attachment; filename= {attachment_file}"
        )

        msg.attach(part)

    s = smtplib.SMTP(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return True


def generate_pdf(data, email):
    with open("/home/hegemon/Kanban/api/application/monthly_report.html") as file_:
        template = Template(file_.read())
        message = template.render(data=data)
        print(message)
        html = HTML(string=message)
        file_name = 'test.pdf'
        html.write_pdf(target=file_name, stylesheets=[
                       "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"])

        send_email(email, subject="Monthly Report",
                   message="Please find the attached Monthly Report", attachment_file=file_name)

        return True

# def generate_csv():


@ celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(
    #     crontab(0, 0, day_of_month='28'), send_monthly_report.s(), name='1st day of every month')
    sender.add_periodic_task(
        crontab(minute=0, hour=19), send_daily_reminder.s(), name='every day 19:30')
    sender.add_periodic_task(
        crontab(minute="*/1"), send_monthly_report.s(), name='1st day of every month')
    # sender.add_periodic_task(
    # crontab(minute="*/1 "), send_daily_reminder.s(), name='every day 19:30')
    # pass


@ celery.task()
def send_monthly_report():
    # send_email with generated pdf
    users = User.query.all()

    for user in users:

        data = data_for_monthly_report(user.id)

        generate_pdf(data, user.email)

    return True


@ celery.task()
def send_daily_reminder():
    users = User.query.all()

    for user in users:

        no_of_pending_tasks_for_the_day = data_for_daily_reminder(user.id)

        print(user.email)

        if no_of_pending_tasks_for_the_day > 0:

            text = 'You have ' + str(no_of_pending_tasks_for_the_day) + \
                ' task/tasks pending. Update the status before EOD.'

            send_email(user.email, "Daily Reminder", text)

    return True


@ celery.task()
def export_card(card_id, user_id):
    # Get data from DB
    card = Card.query.filter_by(id=card_id, user_id=user_id).first()
    user = User.query.filter_by(id=user_id).first()

    df = pd.DataFrame([card.__dict__])
    # https: // stackoverflow.com/a/54459082/11887766

    df.to_csv('card.csv', index=False, header=True)

    send_email(user.email, "Card Export",
               "Please find the CSV of the card attached", "card.csv")

    # Convert to CSV
    # Send using flask
    return "CSV_SENT", 200


@celery.task()
def export_list(list_id, user_id):
    # Get List from DB
    list = List.query.filter_by(id=list_id, user_id=user_id).first()
    user = User.query.filter_by(id=user_id).first()
    data_dict = {
        "list_id": list.id,
        "title": list.title,
        "user_id": list.user_id,
        "card_id": "",
        "card_title": "",
        "card_content": "",
        "completed": "",
        "completed_at": "",
        "created_at": "",
        "last_updated_at": "",
        "deadline": "",
    }
    data = []
    for card in list.cards:
        data_dict['card_id'] = card.id
        data_dict['card_title'] = card.title
        data_dict['card_content'] = card.content
        data_dict['completed'] = card.completed
        data_dict['completed_at'] = card.completed_at
        data_dict['created_at'] = card.created_at
        data_dict['last_updated_at'] = card.last_updated_at
        data_dict['deadline'] = card.deadline
        data.append(dict(data_dict))

    df = pd.DataFrame(data)

    df.to_csv("list.csv", index=False, header=True)

    send_email(user.email, "List Export",
               "Please find the CSV of the list and its constiuent cards attached", "list.csv")

    return "CSV_SENT", 200
