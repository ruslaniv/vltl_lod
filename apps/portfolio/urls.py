from django.urls import path
from .views import PortfolioHomeView

app_name = 'portfolio'

urlpatterns = [
    path('', PortfolioHomeView.as_view(), name='portfolio'),
]