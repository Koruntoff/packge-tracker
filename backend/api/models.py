from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class StorageLocation(models.Model):
    location_code = models.CharField(max_length=20, unique=True)  # e.g., "A1-B2"
    description = models.TextField(blank=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return self.location_code

class Package(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned')
    ]

    tracking_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=2)  # in kg
    location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    arrival_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    barcode_data = models.TextField(blank=True)  # Store additional barcode data

    def __str__(self):
        return f"{self.tracking_number} - {self.customer.name}"

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    packages = models.ManyToManyField(Package)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Invoice #{self.id} - {self.customer.name}"

from django.db import models
from django.utils import timezone

class StorageLocation(models.Model):
    shelf_number = models.CharField(max_length=50, unique=True)
    zone = models.CharField(max_length=50)
    is_occupied = models.BooleanField(default=False)
    capacity = models.IntegerField(default=1)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Shelf {self.shelf_number} ({self.zone})"

class Package(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('received', 'Received'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
    ]

    COURIER_CHOICES = [
        ('fedex', 'FedEx'),
        ('ups', 'UPS'),
        ('usps', 'USPS'),
        ('dhl', 'DHL'),
        ('amazon', 'Amazon Logistics'),
    ]

    tracking_number = models.CharField(max_length=100, unique=True)
    customer_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    courier = models.CharField(max_length=50, choices=COURIER_CHOICES)
    location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    arrival_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    barcode_data = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='package_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.customer_name}"

    class Meta:
        ordering = ['-arrival_date']

class PackageImage(models.Model):
    package = models.ForeignKey(Package, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='package_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.package.tracking_number}"