from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email():
    app = current_app._get_current_object()
    msg = Message("Hello",sender="gtfseditor@gmail.com",recipients=["mardom4164@gmail.com"])
    msg.body = "This mail is send it from Gtfseditor. For more info, please enter......."
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
