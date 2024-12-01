from django.urls import path  # type: ignore
from . import views

urlpatterns = [
    path('', views.index_view, name='home'),  # Home page
    path('about/', views.about_view, name='about'),  # About page
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('login/', views.login_view, name='login'),  # Login page
    path('dataentry/', views.data_entry_view, name='dataentry'),  # Data entry page
    path('result/', views.result, name='result'),  # Result page
]



