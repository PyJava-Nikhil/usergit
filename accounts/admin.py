from django.contrib import admin
from accounts.models import Account
from django.utils.html import mark_safe
# Register your models here.

class AccounntAdmin(admin.ModelAdmin):
    readonly_fields = ['image']
    search_fields = ["date_added", "login"]

    def image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url = obj.user_info["avatar_url"],
                width = 150,
                height = 150
            )
        )

admin.site.register(Account, AccounntAdmin)
