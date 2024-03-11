from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import User
from django.views import View


def is_blocked_user(phone_number):
    user = User.objects.filter(phone_number=phone_number).first()
    return user and user.is_block


class BlockCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect("accounts:user_login_otp")

        if is_blocked_user(user.phone_number):
            messages.error(
                request,
                _("Your account has been blocked. To follow up on this issue, please contact support"),
                "danger",
            )
            logout(request)
            return redirect("accounts:user_login_otp")

        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixin(View):
    """
    Mixin which requires the user to be logged in.
    """
    @method_decorator(login_required(login_url='accounts:user_login_otp'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BlockMixin(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BlockCheckLoginRequiredMixin(BlockCheckMixin, LoginRequiredMixin):
    pass
