from django.urls import path

from rate import views


app_name = "rate"

urlpatterns = [
    path('list/',  views.RateList.as_view(), name='list'),
    path('latest/',  views.LatestRateList.as_view(), name='latest'),
    path('download-csv/',  views.RateDownloadCSV.as_view(), name='download-csv'),
    path('download-xlsx/',  views.RateDownloadXLSX.as_view(), name='download-xlsx'),
    path('edit/<int:pk>/',  views.RateEdit.as_view(), name='edit'),
    path('delete/<int:pk>/',  views.RateDelete.as_view(), name='delete'),
]
