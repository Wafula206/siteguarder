from django.urls import path
from .views import home_view, about_view, scan_view, history_view

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('scanner/', scan_view, name='scan'),
    path('history/', history_view, name='history'),
]