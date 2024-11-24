# backend/api/serializers.py
from rest_framework import serializers
from .models import Package, StorageLocation, PackageImage, ScheduledEvent

class StorageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = '__all__'

class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageImage
        fields = ['id', 'image', 'uploaded_at', 'description']

class PackageSerializer(serializers.ModelSerializer):
    location_details = StorageLocationSerializer(source='location', read_only=True)
    images = PackageImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Package
        fields = '__all__'

class ScheduledEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledEvent
        fields = '__all__'