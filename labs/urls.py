from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /labs/5/
    path('<int:laboratory_id>/', views.detail, name='detail'),
    # ex: /labs/5/send/
    path('<int:laboratory_id>', views.detail, name='send'),
]
