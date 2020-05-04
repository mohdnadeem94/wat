from django.urls import path
from . import views

app_name = 'my_app'

urlpatterns = [
    path('app_page/',views.AppPage,name = 'app_page'),
]
