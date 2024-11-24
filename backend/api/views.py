# backend/api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Package, StorageLocation, PackageImage, ScheduledEvent
from .serializers import (
    PackageSerializer, 
    StorageLocationSerializer, 
    PackageImageSerializer,
    ScheduledEventSerializer
)

class StorageLocationViewSet(viewsets.ModelViewSet):
    queryset = StorageLocation.objects.all()
    serializer_class = StorageLocationSerializer

    @action(detail=False, methods=['get'])
    def available(self):
        locations = self.queryset.filter(is_occupied=False)
        serializer = self.serializer_class(locations, many=True)
        return Response(serializer.data)

class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        package = self.get_object()
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=400)
        
        image = request.FILES['image']
        description = request.data.get('description', '')
        
        package_image = PackageImage.objects.create(
            package=package,
            image=image,
            description=description
        )
        
        serializer = PackageImageSerializer(package_image)
        return Response(serializer.data, status=201)

class ScheduledEventViewSet(viewsets.ModelViewSet):
    queryset = ScheduledEvent.objects.all()
    serializer_class = ScheduledEventSerializer

    @action(detail=False, methods=['get'])
    def filtered(self, request):
        event_type = request.query_params.get('event_type', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        queryset = self.queryset

        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        if start_date:
            queryset = queryset.filter(start_time__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(end_time__lte=end_date)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

@action(detail=False, methods=['get'])
def find_by_tracking(self, request):
    tracking_number = request.query_params.get('number', '')
    # Add your customer matching logic here
    return Response(...)