from django import forms
from .models import OTPCode, User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from common.valid_phone_number import validate_phone_number
from django.shortcuts import get_object_or_404
from common.generate_random_number import generate_random_number
from accounts.tasks import send_login_sms_task
from datetime import datetime, timedelta

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        return password2

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('This phone number is already in use. Please enter another phone number')

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
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'phone number', 'autocomplete': 'off'}),
        error_messages={'required': _('Phone Number field is required')},
    )

    def clean_phone_number(self):
        raw_phone_number = self.cleaned_data['phone_number']
        formatted_phone_number = validate_phone_number(raw_phone_number)

        if not formatted_phone_number or not raw_phone_number.isdigit():
            raise ValidationError(_("The phone number entered is incorrect. Please enter as in the example"))
        else:
            if User.objects.filter(phone_number=formatted_phone_number).exists():
                raise ValidationError(
                    _("The entered phone number is already registered on the site. Please enter another phone number or log in to your account with the entered phone number"))
            verification_code = generate_random_number(4, is_unique=False)
            send_login_sms_task.delay(formatted_phone_number, verification_code)

            OTPCode.objects.filter(phone_number=formatted_phone_number).delete()
            OTPCode.objects.create(
                phone_number=formatted_phone_number,
                code=verification_code,
                expire_time=datetime.now() + timedelta(seconds=120),
            )
            return formatted_phone_number
            

class LoginWithPasswordForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'phone number'}),
        error_messages={'required': _('Phone Number field is required')}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'password'}),
        error_messages={'required': _('Password field is required')}
    )

    def clean_phone_number(self):
        phone_number = validate_phone_number(self.cleaned_data['phone_number'])

        if phone_number:
            user = User.objects.filter(phone_number=phone_number).first()

            if not user:
                raise ValidationError(_("The phone number entered on the site is not registered. Please register first"))

            if user.is_block:
                raise ValidationError(_('Your account has been blocked. To follow up on this issue, please contact support'))

            return phone_number

        raise ValidationError(_("The phone number entered is incorrect. Please enter as in the example"))

    def clean_password(self):
        phone_number = validate_phone_number(self.cleaned_data['phone_number'])
        password = self.cleaned_data['password']
        user = get_object_or_404(User, phone_number=phone_number)

        if not user.has_usable_password():
            raise ValidationError(_("No password has been set for your phone number. Please enter a password in the forgot password section or use a one-time password to log in to your account"))

        if not user.check_password(password):
            raise ValidationError(_("Incorrect password"))

        return password
    

class LoginWithOTPForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'dir': 'ltr',
            'placeholder': 'Phone number',
            'autocomplete': 'off'
        }),
        error_messages={'required': _('Phone Number field is required')}
    )

    def clean_phone_number(self):
        raw_phone_number = self.cleaned_data.get('phone_number')
        formatted_phone_number = validate_phone_number(raw_phone_number)

        if not formatted_phone_number or not raw_phone_number.isdigit():
            raise ValidationError(_("The phone number entered is incorrect. Please enter as in the example"))

        user = User.objects.filter(phone_number=formatted_phone_number).first()

        if not user:
            raise ValidationError(_("The phone number entered on the site is not registered. Please register first"))

        if user.is_block:
            raise ValidationError(_('Your account has been blocked. To follow up on this issue, please contact support'))

        verification_code = generate_random_number(4, is_unique=False)
        send_login_sms_task.delay(formatted_phone_number, verification_code)

        OTPCode.objects.filter(phone_number=formatted_phone_number).delete()
        OTPCode.objects.create(
            phone_number=formatted_phone_number,
            code=verification_code,
            expire_time=datetime.now() + timedelta(seconds=120),
        )

        return formatted_phone_number
        

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'OTP Code', 'autocomplete': 'off'}),
        error_messages={
            'invalid': _('The entered code is incorrect'),
            'required': _('Code field is required'),
            }
        )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VerifyCodeForm, self).__init__(*args, **kwargs)

    def clean_code(self, *args, **kwargs):
        cleaned_data = super().clean()
        code = self.cleaned_data['code']
        
        if not str(code).isdigit():
            raise ValidationError(_('The entered code is incorrect'))
        
        phone_number = self.request.session['phone_number']
        verification_code = OTPCode.objects.get(phone_number=phone_number)
        
        if int(code) == int(verification_code.code):
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


class AddCreditForm(forms.Form):
    amount = forms.CharField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'dir': 'ltr', 'placeholder': 'number',
               'autocomplete': 'off'}),
        error_messages={
            'required': _('Amount field is required'),
            }
        )
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
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
