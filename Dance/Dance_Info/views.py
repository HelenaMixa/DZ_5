from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import connection
from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .forms.forms import CoachForm
from .models import Club, Coach, Dancer
from .serializers import ClubSerializer, DancerSerializer, CoachSerializer


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


class ClubApiListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000


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


# class ClubApiView(APIView):
#     def get(self, request):
#         w = Club.objects.all()
#         return Response({'post': ClubSerializer(w, many=True).data})
#
#     def post (self, request):
#         serializer = ClubSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = Club.objects.get(pk=pk)
#         except:
#             return Response({"error": "Method PUT not allowed"})
#
#         serializer = ClubSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'post': serializer.data})


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


# def dance(request):
#     dances = Dancer.objects.order_by('dancer_surname')
#     page_number = request.GET.get('page')
#     all_dance = Paginator(dances, 3)
#     try:
#         dances_all = all_dance.page_number(page_number)
#     except PageNotAnInteger:
#         dances_all = all_dance.page_number(1)
#     except EmptyPage:
#         dances_all = all_dance.page_number(all_dance.num_pages)

#     return render(request, 'Dance_Info/dancers.html', {'dances_all ': dances_all})


def listing(request):
    contact_list = Dancer.objects.all()
    paginator = Paginator(contact_list, 2)
    page = request.GET.get('page')
    paginator.page_name = "Страница"
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'Dance_Info/pag_dancers.html', {'contacts': contacts})
