from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(SecuredDoor)
admin.site.register(UserSecurityCredential)
admin.site.register(SecurityLog)


admin.site.site_header = "Stores Security System"
admin.site.site_title = "Stores Security "
admin.site.index_title = "Stores Security"