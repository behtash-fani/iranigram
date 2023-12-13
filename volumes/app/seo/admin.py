from django.contrib import admin
from .models import PagesSeo
from django import forms


class PagesSeoAdminForm(forms.ModelForm):
    class Meta:
        model = PagesSeo
        fields = "__all__"
        widgets = {'canonical_link': forms.TextInput(attrs={'dir': 'ltr'})}

@admin.register(PagesSeo)
class PagesSeoAdmin(admin.ModelAdmin):
    form = PagesSeoAdminForm
    list_display = ['page', 'title_tag',]