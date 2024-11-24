from django.contrib import admin
from .models import Package, StorageLocation, PackageImage

admin.site.register(Package)
admin.site.register(StorageLocation)
admin.site.register(PackageImage)