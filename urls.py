from django.urls import path
from . import views

urlpatterns = [
    path('imports', views.ShopUnitAPIView.as_view()),
    path('nodes/<str:uuid>', views.ShopUnitAPIView.as_view()),
    path('delete/<str:uuid>', views.ShopUnitAPIView.as_view())
]