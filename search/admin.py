from django.contrib import admin

from search.models import Corp
from django.db.models.functions import Lower
# Register your models here.
@admin.register(Corp)
class CorpAdmin(admin.ModelAdmin):
    list_display = ('corp_code','corp_name')
    
    def get_ordering(self, request):
        return [Lower('corp_name')]  # sort case insensitive