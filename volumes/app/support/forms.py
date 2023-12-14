from django import forms
from .models import Ticket, Response


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'message', 'file']

    file = forms.ImageField(required=False,
                            widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}))
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Message'}))

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['style'] = 'height:120px;'


class ResponseForm(forms.ModelForm):
    file = forms.ImageField(required=False,
                            widget=forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Image'}))
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Message'}))

    class Meta:
        model = Response
        fields = ['message', 'file']

    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['style'] = 'height:120px;'
