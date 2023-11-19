from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


STATUS_CHANGE_WALLET = (
    ('do_nothing', "---------"),
    ("add_credit", _("Add Credit")),
    ("reduce_credit", _("Reduce Credit")),
)


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=20, unique=True, verbose_name=_('Phone Number'))
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True, verbose_name=_('Email'))
    full_name = models.CharField(default=_('Guest User'), max_length=255, blank=True, null=True,
                                 verbose_name=_('Full Name'))
    balance = models.PositiveIntegerField(default=0, verbose_name=_('Balance'), blank=True, null=True)
    amount_change_wallet = models.PositiveIntegerField(default=0, verbose_name=_('Amount Change Wallet'), blank=True,
                                                       null=True)
    status_change_wallet = models.CharField(max_length=100, choices=STATUS_CHANGE_WALLET, default="do_nothing",
                                            verbose_name=_('Status Change Wallet'))
    description_change_wallet = models.TextField(max_length=2000, default="", blank=True, null=True,
                                                 verbose_name=_('Description Change Wallet'))
    orders_count = models.PositiveBigIntegerField(default='0', blank=True, null=True, verbose_name=_("Order Counts"))
    is_block = models.BooleanField(default=False, verbose_name=_('Block'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_admin = models.BooleanField(default=False, verbose_name=_('Admin'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'

    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin
        
    def add_credit(self, amount):
        self.balance += amount
        self.save()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


@receiver(post_save, sender=User)
def order_count(sender, instance, created, **kwargs):
    user_orders_count = instance.orders.all().count()
    user_instance = User.objects.filter(phone_number=instance.phone_number)
    user_instance.update(orders_count=user_orders_count)
    Token.objects.get_or_create(user=instance)


class OTPCode(models.Model):
    phone_number = models.CharField(max_length=12, verbose_name=_('Phone Number'))
    code = models.CharField(max_length=4, verbose_name=_('Code'))
    expire_time = models.TimeField(blank=True, null=True, verbose_name=_('Expire Time'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Create At'))

    def __str__(self):
        return f'{self.phone_number}'

    class Meta:
        verbose_name = _('OTPCode')
        verbose_name_plural = _('OTPCodes')
