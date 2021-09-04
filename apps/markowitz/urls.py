from django.urls import path
from .views import MarkowitzHomeView

app_name = 'markowitz'

urlpatterns = [
    path('', MarkowitzHomeView.as_view(), name='markowitz'),
]