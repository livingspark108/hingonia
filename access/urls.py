from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    path('add/', CreateRoleView.as_view(), name='add_role'),
    path('edit/<int:pk>/',UpdateRoleView.as_view(), name='edit_role'),
    path('list/', ListRoleView.as_view(), name='list_role'),
    path('list/ajax', ListRoleViewJson.as_view(), name='listajax_role'),
    ]