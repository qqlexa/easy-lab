from django.contrib import admin
from django.urls import include, path

from . import views

app_name = 'labs'

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /labs/5/
    path('<int:laboratory_id>/', views.detail, name='detail'),
    # ex: /labs/5/send/
    path('<int:laboratory_id>', views.detail, name='send'),
    path('new_lab/', views.new_lab, name='new_lab')
]
