from django.urls import path

from . import views
from .views import CoachView

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about),
    path('clubs/', views.club, name='clubs'),
    path('dancers/', views.dancers, name='dancers'),
    path('contact/', CoachView.as_view(), name='coach'),
    path('dance/', views.dance, name='dance'),
    path('Pagination_Dancers/', views.listing, name='Pagination_Dancers'),
]
