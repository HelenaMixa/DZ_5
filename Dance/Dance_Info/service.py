from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination


class PaginationDancer(PageNumberPagination):
    page_size = 2
    max_page_size = 100
    page_size_query_param = 'size'
    page_query_param = 'stranitsa'


def send(user_email):
    send_mail(
        'Operation completed successfully.',
        'elenamikhaylutsa7@gmail.com',
        [user_email],
        fail_silently=False,
    )