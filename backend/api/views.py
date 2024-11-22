from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .models import Customer, StorageLocation, Package, Invoice, Schedule
from .serializers import (CustomerSerializer, StorageLocationSerializer, 
                        PackageSerializer, InvoiceSerializer, ScheduleSerializer)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
    @action(detail=True, methods=['get'])
    def packages(self, request, pk=None):
        customer = self.get_object()
        packages = Package.objects.filter(customer=customer)
        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data)

class StorageLocationViewSet(viewsets.ModelViewSet):
    queryset = StorageLocation.objects.all()
    serializer_class = StorageLocationSerializer
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        locations = StorageLocation.objects.filter(is_occupied=False)
        serializer = self.get_serializer(locations, many=True)
        return Response(serializer.data)

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    @action(detail=False, methods=['post'])
    def scan_barcode(self, request):
        barcode_data = request.data.get('barcode_data')
        try:
            # Process barcode data (you'll need to implement the actual scanning logic)
            tracking_number = barcode_data  # Extract tracking number from barcode
            weight = request.data.get('weight')
            customer_id = request.data.get('customer_id')
            location_id = request.data.get('location_id')

            package = Package.objects.create(
                tracking_number=tracking_number,
                customer_id=customer_id,
                weight=weight,
                location_id=location_id,
                barcode_data=barcode_data
            )
            
            serializer = self.get_serializer(package)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        invoice = self.get_object()
        invoice.paid = True
        invoice.save()
        return Response({'status': 'invoice marked as paid'})

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        schedules = Schedule.objects.filter(
            start_time__date=today
        ).order_by('start_time')
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def dashboard_stats(request):
    stats = {
        'totalPackages': Package.objects.count(),
        'pendingDeliveries': Package.objects.filter(status='pending').count(),
        'totalCustomers': Customer.objects.count(),
        'availableLocations': StorageLocation.objects.filter(is_occupied=False).count()
    }
    
    recent_packages = Package.objects.select_related('customer', 'location').order_by('-arrival_date')[:5]
    recent_packages_data = PackageSerializer(recent_packages, many=True).data
    
    return Response({
        'stats': stats,
        'recent_packages': recent_packages_data
    })
