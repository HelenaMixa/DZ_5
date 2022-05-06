from django.core.mail import send_mail


def send(user_email):
    send_mail(
        'Operation completed successfully.',
        'elenamikhaylutsa7@gmail.com',
        [user_email],
        fail_silently=False,
    )