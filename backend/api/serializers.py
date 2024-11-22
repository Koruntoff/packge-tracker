from rest_framework import serializers
from .models import Customer, StorageLocation, Package, Invoice, Schedule

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class StorageLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageLocation
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    location_code = serializers.CharField(source='location.location_code', read_only=True)

    class Meta:
        model = Package
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    package_count = serializers.IntegerField(source='packages.count', read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.get_full_name', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'