from django.urls import path
from .views import CompanyApiView

urlpatterns = [
    path('car_parts', CompanyApiView.as_view()),
]