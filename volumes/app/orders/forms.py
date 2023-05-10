from django import forms
from orders.models import Order
from service.models import Service, ServiceType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from accounts.models import User
from common.valid_phone_number import validate_phone_number

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        ordering = ["priority"]
        fields = ["service_type", "service", "link", "quantity"]
        widgets = {
            "service_type": forms.Select(attrs={"class": "form-select"}),
            "service": forms.Select(attrs={"class": "form-select"}),
            "link": forms.TextInput(
                attrs={
                    "class": "form-control text-left",
                    "dir": "ltr",
                    "autocomplete": "off",
                }
            ),
            "quantity": forms.TextInput(
                attrs={
                    "class": "form-control text-left",
                    "dir": "ltr",
                    "type": "number",
                    "autocomplete": "off",
                }
            ),
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
        if link is None:  # if link field is empty raise error
            raise forms.ValidationError(_("Please enter a instagram public link/id"))
        service = self.cleaned_data["service"]
        result_compare = 0
        if service.link_type == "instagram_post_link":  # check  type link of user order
            link_pattern = [
                "https://www.instagram.com",
                "https://instagram.com",
                "instagram.com",
                "www.instagram.com",
            ]
            for pattern in link_pattern:
                if link.startswith(pattern):
                    result_compare += 1
                    return link
            if result_compare == 0:
                raise forms.ValidationError(
                    _("The link entered is not a valid Instagram post link")
                )
        return link

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity is None:
            raise forms.ValidationError(_("Please enter quantity of order"))
        return quantity



class TemplateOrderForm(forms.Form):
    user = ''
    link = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control text-left",
                "dir": "ltr",
                "placeholder": "Instagram Link",
                "autocomplete": "off",
            }
        ),
    )
    phone_number = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "dir": "ltr",
                "placeholder": "Phone Number",
                "autocomplete": "off",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TemplateOrderForm, self).__init__(*args, **kwargs)

    def clean_link(self):
        link = self.cleaned_data["link"]
        if link is None:  # if link field is empty raise error
            raise forms.ValidationError(_("Please enter a instagram public link/id"))
        service_id = self.request.session["service_id"]
        service = Service.objects.get(id=service_id)
        result_compare = 0
        if service.link_type == "instagram_post_link":  # check type link of user order
            link_pattern = [
                "https://www.instagram.com",
                "https://instagram.com",
                "instagram.com",
                "www.instagram.com",
            ]
            for pattern in link_pattern:
                if link.startswith(pattern):
                    result_compare += 1
                    return link
            if result_compare == 0:
                raise forms.ValidationError(
                    _("The link entered is not a valid Instagram post link")
                )
        return link


    def clean_phone_number(self):
        if not self.cleaned_data["phone_number"]:
            raise ValidationError("Phone Number field is required.")
        
        phone_number = self.cleaned_data["phone_number"]
        phone_number = validate_phone_number(phone_number)

        if phone_number:
            if not User.objects.filter(phone_number=phone_number).exists():
                raise ValidationError(
                    _(
                        "The phone number entered on the site is not registered. Please register first"
                    )
                )
            elif User.objects.get(phone_number=phone_number).is_block:
                raise ValidationError(
                    _(
                        "Your account has been blocked. To follow up on this issue, please contact support"
                    )
                )
            else:
                return phone_number
        else:
            raise ValidationError(
                _(
                    "The phone number entered is incorrect. Please enter as in the example"
                )
            )