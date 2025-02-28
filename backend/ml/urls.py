from django.urls import path
from .views import rank_shops

urlpatterns = [
    path("rank_shops/", rank_shops, name="rank_shops"),
]