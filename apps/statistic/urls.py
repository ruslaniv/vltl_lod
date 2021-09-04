from django.urls import path
from .views import StatsHomeView

app_name = 'statistics'

urlpatterns = [
    path('', StatsHomeView.as_view(), name='statistics'),
]