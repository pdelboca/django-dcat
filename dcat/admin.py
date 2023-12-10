from django.contrib import admin

# Register your models here.

from dcat.models import (
    Catalog,
    Dataset,
    Distribution,
    Agent,
    MediaType,
    LicenceDocument,
    DataTheme,
)

admin.site.register(Catalog)


class DatasetAdmin(admin.ModelAdmin):
    search_fields = ("title",)


admin.site.register(Dataset, DatasetAdmin)


class DistributionAdmin(admin.ModelAdmin):
    search_fields = ("title",)


admin.site.register(Distribution, DistributionAdmin)
admin.site.register(Agent)
admin.site.register(MediaType)
admin.site.register(LicenceDocument)
admin.site.register(DataTheme)
