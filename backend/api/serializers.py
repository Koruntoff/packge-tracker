from rest_framework import serializers
from .models import Package, StorageLocation, PackageImage

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
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Package
        fields = '__all__'
        extra_fields = ['location_details', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        package = Package.objects.create(**validated_data)
        
        for image in uploaded_images:
            PackageImage.objects.create(package=package, image=image)
        
        return package