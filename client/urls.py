from django.urls import path
from .views import ClientApiView, ClientApiPurchasedView

urlpatterns = [
    path('parts', ClientApiView.as_view()),
    path('parts/<int:car_part_id>', ClientApiView.as_view()),
    path('parts/items', ClientApiPurchasedView.as_view()),
]