from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from common.mixins import LoginRequiredMixin
from common.is_block_user import is_block_user
from django.contrib.auth import logout


class BlockCheckMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect("accounts:user_login_otp")
        if is_block_user(user.phone_number):
            messages.error(
                request,
                _("Your account has been blocked. To follow up on this issue, please contact support"),
                "danger",
            )
            logout(request)
            return redirect("accounts:user_login_otp")
        return super().dispatch(request, *args, **kwargs)


class BlockCheckLoginRequiredMixin(BlockCheckMixin, LoginRequiredMixin):
    pass
