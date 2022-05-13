from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import connection
from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .forms.forms import CoachForm
from .models import Club, Coach, Dancer
from .serializers import ClubSerializer, DancerSerializer, CoachSerializer
from .service import PaginationDancer


def arab_to_roman(n):
    result = ''
    for arabic, roman in zip((1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1),
                             'M     CM   D    CD   C    XC  L   XL  X   IX V  IV I'.split()):
        result += n // arabic * roman
        n %= arabic
    return result


def roman_to_arab(roman):
    _rdecode = dict(zip('MDCLXVI', (1000, 500, 100, 50, 10, 5, 1)))
    result = 0
    for r, r1 in zip(roman, roman[1:]):
        rd, rd1 = _rdecode[r], _rdecode[r1]
        result += -rd if rd < rd1 else rd
    return result + _rdecode[roman[-1]]


def listing(request, **kwarqs):
    contact_list = Dancer.objects.order_by('dancer_surname').all()
    paginator = Paginator(contact_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
        arabstr = roman_to_arab(page)
        contacts = paginator.page(arabstr)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    i = contacts.number
    page_pre = arab_to_roman(i-1)
    page_next = arab_to_roman(i+1)
    page_curr = arab_to_roman(i)
    page_total = arab_to_roman(contacts.paginator.num_pages)
    return render(request, 'dance_info/pag_dancers.html',
                  {'title': 'База данных танцоров. Пагинация',
                   'contacts': contacts,
                   'page_pre': page_pre,
                   'page_next': page_next,
                   'page_curr': page_curr,
                   'page_total': page_total})


class DancersRecordsView(generics.ListAPIView):
    queryset = Dancer.objects.all()
    serializer_class = DancerSerializer
    pagination_class = PaginationDancer


class ClubApiListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class GoodsListView(viewsets.ReadOnlyModelViewSet):
    queryset = Club.objects.all().select_related('coach')
    serializer_class = ClubSerializer
    pagination_class = PaginationDancer


class ClubApiList(generics.ListAPIView):
    queryset = Club.objects.all().select_related('coach')
    serializer_class = ClubSerializer
    pagination_class = ClubApiListPagination


class DancerAPIView(generics.ListAPIView):
    queryset = Dancer.objects.all()
    serializer_class = DancerSerializer


class ClubAPIView(generics.ListAPIView):
    queryset = (
        Club.objects
            .filter(club_name='Prestige')
            .select_related('couch')
            .values('club_name', 'city')
    )
    serializer_class = ClubSerializer


class CoachView(CreateView):
    model = Coach
    form_class = CoachForm
    success_url = 'contact/'
    template_name = 'Dance_Info/contact.html'

    def form_valid(self, form, send_spam_email=None):
        form.save()
        send_spam_email.delay(form.instance.email)
        return super().form_valid(form)


def index(request):
    return render(request, 'Dance_Info/index.html')


def club(request):
    clubs = Club.objects.filter(club_name='Marich')
    return render(request, 'Dance_Info/club.html', {'clubs': clubs})


class ClubApiList(generics.ListAPIView):
    queryset = Club.objects.all().select_related('coach')
    serializer_class = ClubSerializer
    pagination_class = ClubApiListPagination

    def list(self, request, *args, **kwargs):
        print(f"BEFORE WAS len({connection.queries}")
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print(f"AFTER WAS len({connection.queries}")
        return Response(serializer.data)


class ClubApiUpdate(generics.UpdateAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class ClubApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer


class CoachApiList(generics.ListCreateAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer


class CoachApiUpdate(generics.UpdateAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer


class CoachApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer


class DancerApiListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DancerApiList(generics.ListCreateAPIView):
    queryset = Dancer.objects.all()
    serializer_class = DancerSerializer
    pagination_class = DancerApiListPagination


class DancerApiUpdate(generics.UpdateAPIView):
    queryset = Dancer.objects.select_related('coach')
    serializer_class = ClubSerializer


def start(request):
    return render(request, 'Dance_Info/index.html')


def about(request):
    return render(request, 'Dance_Info/Hello.html')


def dancers(request):
    show_dancers = Dancer.objects.order_by('club')
    return render(request, 'Dance_Info/dancers.html',
                  {'title': 'База данных танцоров', 'dancers': show_dancers})


def coach(request):
    show_coach = Coach.objects.all()
    return render(request, 'Dance_Info/coach.html',
                  {'title': 'База данных тренеров', 'coaches': show_coach})


def dance(request):
    dances = Dancer.objects.order_by('dancer_surname')
    page_number = request.GET.get('page')
    all_dance = Paginator(dances, 3)
    try:
        dances_all = all_dance.page_number(page_number)
    except PageNotAnInteger:
        dances_all = all_dance.page_number(1)
    except EmptyPage:
        dances_all = all_dance.page_number(all_dance.num_pages)
    return render(request, 'Dance_Info/dancers.html', {'dances_all ': dances_all})


# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#
# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3)  # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'blog/post/list.html',
#                   {'page': page,
#                    'posts': posts})
