from django.urls import path
from api.clients.views import ClientList

urlpatterns = [path('', ClientList.as_view())]
