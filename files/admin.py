from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    readonly_fields = ('url', 'created_by', 'created_time', 'last_modified_by', 'last_modified_time')
    list_display = ('__str__', 'url')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        self.request = request  # used for building absolute url for files
        return super().get_queryset(request)

    def url(self, obj):
        return self.request.build_absolute_uri(obj.file.url)
