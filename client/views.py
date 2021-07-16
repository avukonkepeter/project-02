from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from client.models import Address, Client


class HomeView(TemplateView):
    template_name = "home.html"


class ClientList(ListView):
    model = Client
    template_name = "client_list.html"


class ClientDetailView(DetailView):
    model = Client
    template_name = "client_details.html"
