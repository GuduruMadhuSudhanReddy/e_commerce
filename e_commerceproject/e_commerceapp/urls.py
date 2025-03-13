from django.urls import path
from e_commerceapp import views

urlpatterns = [
    path('', views.index, name="index"),      # No leading '/' and simplified name
    path('contact/', views.contact, name="contact"),
    path('about/', views.about, name="about"), # Remove leading '/' and use a descriptive name
    path('checkout/', views.checkout, name="checkout"), 
]
