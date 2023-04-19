from django import forms
from .models import OTPCode, User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from utils.valid_phone_number import validate_phone_number
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, logout, login



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number',)

    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd["password1"]
        password2 = cd["password2"]
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number).exists()
        if user:
            raise ValidationError('this phone number is already exist, please enter another phone number')
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone_number', 'password', 'last_login')


class UserRegisterWithOTPForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'phone number', 'autocomplete': 'off'}))

    def clean_phone_number(self):

        if not self.cleaned_data['phone_number']:
            raise ValidationError("Phone Number field is required.")

        phone_number = validate_phone_number(self.cleaned_data['phone_number'])
        if phone_number:
            if User.objects.filter(phone_number=phone_number).exists():
                raise ValidationError(
                    _("The entered phone number is already registered on the site. Please enter another phone number or log in to your account with the entered phone number"))
            return phone_number
        else:
            raise ValidationError(_("The phone number entered is incorrect. Please enter as in the example"))


class LoginWithOTPForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'phone number', 'autocomplete': 'off'}))

    def clean_phone_number(self):

        if not self.cleaned_data['phone_number']:
            raise ValidationError("Phone Number field is required.")

        phone_number = validate_phone_number(self.cleaned_data['phone_number'])

        if phone_number:
            if not User.objects.filter(phone_number=phone_number).exists():
                raise ValidationError(
                    _("The phone number entered on the site is not registered. Please register first"))
            elif User.objects.get(phone_number=phone_number).is_block:
                raise ValidationError(_('Your account has been blocked. To follow up on this issue, please contact support'))
            else:
                return phone_number
        else:
            raise ValidationError(_("The phone number entered is incorrect. Please enter as in the example"))


class LoginWithPasswordForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'phone number'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'password'}))
    

    def clean_phone_number(self):

            if not self.cleaned_data['phone_number']:
                raise ValidationError("Phone Number field is required.")

            phone_number = validate_phone_number(self.cleaned_data['phone_number'])

            if phone_number:
                if not User.objects.filter(phone_number=phone_number).exists():
                    raise ValidationError(
                        _("The phone number entered on the site is not registered. Please register first"))
                elif User.objects.get(phone_number=phone_number).is_block:
                    raise ValidationError(_('Your account has been blocked. To follow up on this issue, please contact support'))
                else:
                    return phone_number
            else:
                raise ValidationError(_("The phone number entered is incorrect. Please enter as in the example"))
            
    def clean_password(self):
        phone_number = validate_phone_number(self.cleaned_data['phone_number'])
        password = self.cleaned_data['password']
        user = get_object_or_404(User, phone_number=phone_number)
        if not user.has_usable_password():
            raise ValidationError(_("No password has been set for your phone number. Please enter a password in the forgot password section or use a one-time password to log in to your account"))
        elif not user.check_password(password):
            raise ValidationError(_("Incorrect password"))
        return password

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'OTP Code', 'autocomplete': 'off'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VerifyCodeForm, self).__init__(*args, **kwargs)

    def clean_code(self, *args, **kwargs):
        cleaned_data = super().clean()
        code = cleaned_data['code']
        phone_number = self.request.session['phone_number']
        verification_code = OTPCode.objects.get(phone_number=phone_number)

        if not code:
            raise ValidationError("Code field is required.")
        
        if code == verification_code.code:
            verification_code.delete()
            return code
        else:
            raise ValidationError(_('The entered code is incorrect'))
        

class EditProfileForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'full name'}))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'email'}))

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].required = False
        self.fields['email'].required = False
    
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError
    #     return email


class AddCreditForm(forms.Form):
    amount = forms.CharField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'number',
               'autocomplete': 'off'}))
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if not amount:
            raise ValidationError("amount field is required.")
        return amount

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'Password', 'autocomplete': 'off'}))
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': _('Password Confirmation'), 'autocomplete': 'off'}))

    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd["password1"]
        password2 = cd["password2"]
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
