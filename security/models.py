from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserSecurityCredential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    card_name = models.CharField(
        max_length=200, 
        null=True,
        verbose_name=_("RFID card holder name")
    )
    card_uid = models.CharField(
        max_length=200, 
        null=True,
        verbose_name=_('RFID card unique identifier')
    )
    user_qr_code = models.ImageField(
        upload_to='user_qr_codes/', 
        null=True,
        verbose_name=_("Security QR code"),
        blank=True
    )
    is_active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date security credentials were created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date sub-product updated"),
        help_text=_("format: Y-m-d H:M:S"),
    ) 

    def __str__(self):
        return self.card_name
    
    def create_qr_code(self):
        pass


class SecuredDoor(models.Model):
    door_name = models.CharField(
        max_length=200, 
        null=True
    )
    door_number = models.PositiveIntegerField(null=True)
    permitted_users = models.ManyToManyField(UserSecurityCredential, related_name='permitted_user_list', blank=True)
    is_active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date security credentials were created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date sub-product updated"),
        help_text=_("format: Y-m-d H:M:S"),
    ) 

    def __str__(self):
        return self.door_name


class SecurityLog(models.Model):
    door = models.ForeignKey(
        SecuredDoor, 
        on_delete=models.CASCADE, 
        null=True
    )
    access_pass = models.ForeignKey(UserSecurityCredential, on_delete=models.CASCADE, null=True)
    session_id = models.CharField(max_length=200, null=True)
    entry_img = models.CharField(max_length=100, null=True)
    entry_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date and time at which staff entered the room"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    entry_status = models.BooleanField(null=True)
    exit_img = models.CharField(max_length=100, null=True)
    exit_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("date and time at which staff exited the room"),
        help_text=_("format: Y-m-d H:M:S"),
    ) 
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date security credentials were created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date sub-product updated"),
        help_text=_("format: Y-m-d H:M:S"),
    ) 

    def __str__(self):
        return self.session_id
