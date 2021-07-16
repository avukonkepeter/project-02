from django.urls import path

from client.views import ClientDetailView, ClientList, HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("clients/", ClientList.as_view(), name="client_list"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
]
