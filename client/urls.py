from django.urls import path
from .views import ClientApiView, ClientApiPurchasedView

urlpatterns = [
    path('shopping', ClientApiView.as_view()),
    path('shopping/<int:car_part_id>', ClientApiView.as_view()),
    path('shopping/purchase', ClientApiPurchasedView.as_view()),
]