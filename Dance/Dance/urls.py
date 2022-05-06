from django.contrib import admin
from django.urls import path, include
from Dance_Info.views import *
from Dance_Info import views
from Dance_Info.views import CoachView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/clublist/', ClubApiList.as_view()),
    path('api/v1/coachlist/', CoachApiList.as_view()),
    path('api/v1/clubdetail/<int:pk>/', ClubApiDetailView.as_view()),
    path('api/v1/dancerlist/', DancerApiList.as_view()),
    path('api/v1/coachdetail/<int:pk>/', CoachApiDetailView.as_view()),
    path('', views.index, name='index'),
    path('club/', views.club, name='club'),
    path('coach/', CoachView.as_view(), name='coach'),
    path('', include('Dance_Info.urls')),
    path('clubs/', include('Dance_Info.urls')),
    path('contact/', include('Dance_Info.urls')),
    path('api/dancer/', DancerAPIView.as_view()),
    path('api/club/', ClubAPIView.as_view()),
    path('dance/', include('Dance_Info.urls')),
    path('dances/', views.dance, name='dances'),
    ]
