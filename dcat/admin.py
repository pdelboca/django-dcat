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
    Keyword,
)


class DatasetAdmin(admin.ModelAdmin):
    search_fields = ("title",)


class DistributionAdmin(admin.ModelAdmin):
    search_fields = ("title",)


class KeywordAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


class DataThemeAdmin(admin.ModelAdmin):
    search_fields = ("label",)


admin.site.register(Catalog)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(Distribution, DistributionAdmin)
admin.site.register(Agent)
admin.site.register(MediaType)
admin.site.register(LicenceDocument)
admin.site.register(DataTheme)
admin.site.register(Keyword, KeywordAdmin)
