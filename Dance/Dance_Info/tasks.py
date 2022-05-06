from Dance.celery import app

from django.core.mail import send_mail

from .models import Coach
from .service import send


@app.task
def send_spam_email(user_email):
    send(user_email)


@app.task
def send_beat_email():
    for contact in Coach.objects.all():
        send_mail(
            'Automatic distribution!',
            'elenamikhaylutsa7@gmail.com',
            [contact.email],
            fail_silently=False,
        )

