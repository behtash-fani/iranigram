from django import forms
from orders.models import Order
from service.models import Service
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from accounts.models import User


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service_type', 'service', 'link', 'quantity']
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'link': forms.TextInput(attrs={'class': 'form-control text-left', 'dir': 'ltr', 'autocomplete': 'off'}),
            'quantity': forms.TextInput(
                attrs={'class': 'form-control text-left', 'dir': 'ltr', 'type': 'number', 'autocomplete': 'off'}),
        }
        error_messages = {
            'link': {
                'required': _('Please enter a valid Instagram link'),
            },
            'quantity': {
                'required': _('Please select the number of orders you want according to the service limit'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.none()

        if 'service_type' in self.data:
            try:
                service_type_id = int(self.data.get('service_type'))
                self.fields['service'].queryset = Service.objects.filter(service_type_id=service_type_id).all()
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['service'].queryset = self.instance.service_type.service_set.order_by('name')

    def clean_service_type(self):
        service_type = self.cleaned_data["service_type"]
        if service_type is None:
            raise forms.ValidationError(_('Please select the type of service'))
        return service_type

    def clean_service(self):
        service = self.cleaned_data["service"]
        if service is None:
            raise forms.ValidationError(_('Please select the service'))
        return service

    def clean_link(self):
        link_pattern = ["https://www.instagram.com", "https://instagram.com", "instagram.com", "www.instagram.com"]
        link = self.cleaned_data["link"]
        result_compare = 0
        if link:
            for pattern in link_pattern:
                if link.startswith(pattern):
                    return link
            if result_compare == 0:
                raise forms.ValidationError(_("The link entered is not a valid Instagram post link"))
        return link

