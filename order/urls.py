from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("confirmation/<int:order_id>/", views.confirmation, name="confirmation"),
    path("history/", views.history, name="history"),
]
