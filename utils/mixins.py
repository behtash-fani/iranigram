from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin:
    """
    Mixin which requires the user to be logged in.
    """

    @method_decorator(login_required(login_url='accounts:user_login_otp'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class BlockMixin:
    # @method_decorator(login_required(login_url='accounts:user_login_otp'))
    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_block:
        #     return redirect('accounts:user_login_otp')
        return super().dispatch(request, *args, **kwargs)
