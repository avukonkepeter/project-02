from django import forms


from client.models import Client, Address, Relationship


class ClientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = Client
        fields = '__all__'


class AddressForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Address
        exclude = ('client', 'id')


class RelationshipForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['relation'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Relationship
        exclude = ('id', )


AddressFormset = forms.modelformset_factory(
    Client, AddressForm, exclude=('client', 'id')
)

AddressInlineFormset = forms.inlineformset_factory(
    Client, Address, form=AddressForm, max_num=2, extra=2,
    min_num=1
)
