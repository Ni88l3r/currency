from django.urls import path

from rate import views


app_name = "rate"

urlpatterns = [
    path('show/', views.show, name='show'),
]
