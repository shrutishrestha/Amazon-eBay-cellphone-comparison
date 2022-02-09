from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('phone/<int:phone_id>/', views.phone_compare, name='phone_compare'),
    path('review/<int:id>/', views.phone_review, name='phone_review'),
]