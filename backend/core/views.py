from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, filters
from django.db.models import Q
from .models import District, Farm, Herd
from .serializers import DistrictSerializer, FarmSerializer, HerdSerializer


@api_view(['GET'])
def health(request):
    return Response({"status": "ok"})


@api_view(['GET'])
def api_root(request):
    """
    Root endpoint providing API information
    """
    return Response({
        "message": "Akyl Jer Government Portal API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health/",
            "districts": "/api/districts/",
            "farms": "/api/farms/",
            "admin": "/admin/"
        }
    })


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing districts only (read-only)
    """
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class FarmViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving farms with filtering support
    
    Query Parameters:
    - district: Filter by district code
    - search: Search in farmer_name or phone (case-insensitive)
    """
    queryset = Farm.objects.select_related('district').prefetch_related('herds').all()
    serializer_class = FarmSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by district code
        district_code = self.request.query_params.get('district', None)
        if district_code:
            queryset = queryset.filter(district__code=district_code)
        
        # Search in farmer_name or phone
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(farmer_name__icontains=search) | Q(phone__icontains=search)
            )
        
        return queryset
