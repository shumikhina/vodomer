from django.contrib import admin

from providers import models

admin.site.register(models.Client)
admin.site.register(models.Provider)
admin.site.register(models.ProviderValue)
