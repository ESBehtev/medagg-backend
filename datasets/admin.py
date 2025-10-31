from django.contrib import admin

from .models import AnatomicalArea, Dataset, MLTask, Modality, Tag

admin.site.register(AnatomicalArea)
admin.site.register(Dataset)
admin.site.register(MLTask)
admin.site.register(Modality)
admin.site.register(Tag)
