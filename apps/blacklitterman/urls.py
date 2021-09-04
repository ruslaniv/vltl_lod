from django.urls import path
from .views import BlackHomeView

app_name = 'blacklitterman'

urlpatterns = [
    path('', BlackHomeView.as_view(), name='blacklitterman'),
]