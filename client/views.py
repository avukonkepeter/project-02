from django.http import JsonResponse
from django.views.generic import DetailView, ListView, TemplateView, UpdateView, CreateView
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404


from client.models import Client, Relationship
from client.forms import ClientForm, AddressInlineFormset, RelationshipForm
from client.utils import id_validator


class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        return context


class HomeView(TemplateView):
    template_name = "home.html"


class ClientList(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientFormView(CreateView):
    model = Client
    form_class = ClientForm
    formset = AddressInlineFormset

    def form_valid(self, form):
        context = self.get_context_data()
        formsets = context['formset']
        self.object = form.save()
        if formsets.is_valid():
            formsets.instance = self.object
            formsets.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = self.formset(self.request.POST)
        else:
            context['formset'] = self.formset()
        return context


class ClientFormViewUpdate(UpdateView):
    form_class = ClientForm
    formset = AddressInlineFormset
    model = Client

    def form_valid(self, form):
        context = self.get_context_data()
        formsets = context['formset']
        if formsets.is_valid():
            response = super().form_valid(form)
            formsets.instance = self.object
            formsets.save()
            return response
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = self.formset(self.request.POST, instance=self.object)
            context['formset'].full_clean()
        else:
            context['formset'] = self.formset(instance=self.object)
        return context


class ClientAutoComplete(JSONResponseMixin, ListView):
    queryset = Client.objects.all()
    template_name = 'client/clients_list_partial.html'

    def render_to_response(self, context, **response_kwargs):
        # Allow both here as we'll also return snippets of the rendered
        # html, which can be used for dynamic replacement of front-end
        if not self.request.GET.get('format') == 'json':
            context = {
                'html_data': render_to_string(self.template_name, context)
            }
        return self.render_to_json_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('term'):
            search_term = self.request.GET.get('term')
            queryset = queryset.annotate(
                full_name=Concat(F('first_name'), Value(' '), F('last_name'))
            ).filter(
                Q(id_number__icontains=search_term) | Q(full_name__icontains=search_term)
            )
        return queryset


class ClientCheckID(JSONResponseMixin, ListView):
    # This can be done via DetailView as well
    queryset = Client.objects.all()

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('id_number'):
            id_number = self.request.GET.get('id_number')
            queryset = queryset.filter(id_number__iexact=id_number)
        return queryset

    def get_data(self, context):
        obj_list = context['object_list']
        data = {'exists': False, 'message': 'This id_number does not exist on the system'}
        if obj_list and obj_list.all():
            data['exists'] = True
            data['message'] = 'This id number exists on the system, please ' \
                              'try again'
        return data


class ClientValidateID(JSONResponseMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        id_number = request.GET.get('id_number', '')
        message = 'This ID Number is valid.'
        is_valid = id_validator(id_number)
        if not is_valid:
            message = 'This ID Number is not valid, please try again.'
        data = {'is_valid': is_valid, 'message': message}
        return self.render_to_json_response(data)


class RelationShipFormView(CreateView):
    model = Relationship
    form_class = RelationshipForm

    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        relation = get_object_or_404(Client, pk=self.kwargs.get('pk'))
        initial['relation'] = relation
        return initial

    def get_form(self, form_class=None, *args, **kwargs):
        form = super().get_form(form_class=form_class)
        if form.is_bound == False:
            form.fields['related_to'].queryset = form.fields['related_to'].queryset.exclude(id=self.kwargs.get('pk'))
        return form
