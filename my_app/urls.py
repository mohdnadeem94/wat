from django.urls import path
from . import views

urlpatterns = [
    path('app_page/',views.AppPage,name = 'app_page'),
]
