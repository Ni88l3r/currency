from account import views

from django.urls import path


app_name = "account"

urlpatterns = [
    path('test/', views.test, name='test'),
]
