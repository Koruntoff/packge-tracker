from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Package, StorageLocation, PackageImage
from .serializers import PackageSerializer, StorageLocationSerializer, PackageImageSerializer

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

    @action(detail=True, methods=['post'])
    def scan_barcode(self, request, pk=None):
        try:
            barcode_data = request.data.get('barcode_data')
            package = get_object_or_404(Package, pk=pk)
            package.barcode_data = barcode_data
            package.save()
            
            serializer = self.get_serializer(package)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['post'])
    def lookup_barcode(self, request):
        barcode = request.data.get('barcode')
        try:
            # Here you would typically integrate with a courier's API
            # For now, we'll just return some dummy data
            package_info = {
                'tracking_number': barcode,
                'courier': 'fedex',
                'weight': 1.5,
                # Add other fields as needed
            }
            return Response(package_info)
        except Exception as e:
            return Response({'error': str(e)}, status=400)