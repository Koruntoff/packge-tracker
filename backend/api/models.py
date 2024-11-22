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

class Schedule(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title