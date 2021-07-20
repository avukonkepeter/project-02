from django.urls import path

from client.views import ClientDetailView, ClientList, HomeView, \
    ClientFormView, ClientFormViewUpdate, ClientAutoComplete, ClientCheckID,\
    ClientValidateID, RelationShipFormView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("clients/", ClientList.as_view(), name="client_list"),
    path("clients/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("clients/<int:pk>/add_relation", RelationShipFormView.as_view(), name="client_add_relationship"),
    path("clients/add/", ClientFormView.as_view(), name="client_add"),
    path("clients/<int:pk>/edit", ClientFormViewUpdate.as_view(), name="client_edit"),
    path('ajax/search_clients/', ClientAutoComplete.as_view()),
    path('ajax/check_id/', ClientCheckID.as_view()),
    path('ajax/validate_id/', ClientValidateID.as_view()),
]
