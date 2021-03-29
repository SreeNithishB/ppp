from django.urls import path
from . import views

urlpatterns = [
    path('restaurant_reviews_logistic/', views.restaurant_reviews_logistic, name='restaurant_reviews_logistic'),
]
