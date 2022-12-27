from django.urls import path
from . import views

urlpatterns = [
    path('/solve',views.say_hello)
]