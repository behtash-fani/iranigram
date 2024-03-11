from django import forms
from orders.models import Order
from service.models import Service, ServiceType
from django.utils.translation import gettext as _


class OrderForm(forms.ModelForm):
    use_wallet = forms.BooleanField(
        required=False, initial=False, label='use wallet', widget=forms.CheckboxInput(attrs={"class": "form-check-input", "placeholder": "Use Wallet"}))
    discount = forms.CharField(required=False, label='discount', widget=forms.TextInput(
        attrs={"class": "form-control text-left", "dir": "ltr", "autocomplete": "off", "placeholder":"Discount", "style": "font-family:VazirCodeHack"}))

    class Meta:
        model = Order
        ordering = ["priority"]
        fields = ["service_type", "service", "link",
                  "quantity", "discount", "use_wallet"]
        widgets = {
            "service_type": forms.Select(attrs={"class": "form-select"}),
            "service": forms.Select(attrs={"class": "form-select"}),
            "link": forms.TextInput(
                attrs={
                    "class": "form-control text-left",
                    "dir": "ltr",
                    "autocomplete": "off",
                    "placeholder":"link",
                    "style": "font-family:VazirCodeHack"
                }
            ),
            "quantity": forms.TextInput(
                attrs={
                    "class": "form-control text-left",
                    "dir": "ltr",
                    "type": "number",
                    "autocomplete": "off",
                    "placeholder":"quantity"
                }
            )
        }
        error_messages = {
            "link": {
                "required": _("Please enter a valid Instagram link"),
            },
            "quantity": {
                "required": _(
                    "Please select the number of orders you want according to the service limit"
                ),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service_type"].queryset = ServiceType.objects.all().order_by(
            "priority"
        )
        self.fields["service"].queryset = Service.objects.none()

        if "service_type" in self.data:
            try:
                service_type_id = int(self.data.get("service_type"))
                self.fields["service"].queryset = Service.objects.filter(
                    service_type_id=service_type_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["service"].queryset = self.instance.service_type.service_set

    def clean_service_type(self):
        service_type = self.cleaned_data["service_type"]
        if service_type is None:
            raise forms.ValidationError(_("Please select the type of service"))
        return service_type

    def clean_service(self):
        service = self.cleaned_data["service"]
        if service is None:
            raise forms.ValidationError(_("Please select the service"))
        return service

    def clean_link(self):
        link = self.cleaned_data["link"]
        if link is None:
            raise forms.ValidationError(
                _("Please enter a instagram public link/id"))
        if "@" in str(link):
            link = link.replace("@", '')
        if ' ' in str(link):
            link = str(link).replace(' ', '')
        return link

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity is None:
            raise forms.ValidationError(_("Please enter quantity of order"))
        return quantity


class TemplateNewOrderForm(forms.ModelForm):
    acceptـtheـrules = forms.BooleanField(
        error_messages={'required': _("Please read and check the rules before placing an order")},required=True, initial=False, label='accept the rules', widget=forms.CheckboxInput(attrs={"class": "form-check-input mt-2",}))
    use_wallet = forms.BooleanField(
        required=False, initial=False, label='use wallet', widget=forms.CheckboxInput(attrs={"class": "form-check-input", "placeholder": "Use Wallet"}))
    discount = forms.CharField(required=False, label='discount', widget=forms.TextInput(
        attrs={"class": "form-control text-left", "dir": "ltr", "autocomplete": "off", "placeholder":"Discount", "style": "font-family:VazirCodeHack"}))

    class Meta:
        model = Order
        fields = ["link", "discount", "use_wallet", 'acceptـtheـrules']
        widgets = {
            "link": forms.TextInput(
                attrs={
                    "class": "form-control text-left",
                    "dir": "ltr",
                    "autocomplete": "off",
                    "placeholder": "Enter Instagram Public Link/ID ",
                    "aria-describedby": "basic-addon4",
                    "style": "font-family:VazirCodeHack"
                }
            ),
        }
        error_messages = {
            "link": {
                "required": _("Please enter a valid Instagram link"),
            },
        }

    def clean_link(self):
        link = self.cleaned_data["link"]
        if link is None:
            raise forms.ValidationError(
                _("Please enter a instagram public link/id"))
        return link
