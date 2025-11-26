from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from django.db.models import Q
from .models import District, Farm, Herd, Event
from .serializers import DistrictSerializer, FarmSerializer, HerdSerializer, EventSerializer


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
            "events": "/api/events/",
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


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and updating events
    
    Query Parameters:
    - district: Filter by district code
    - event_type: Filter by event type (disease_outbreak, vaccination, inspection, quarantine)
    - status: Filter by status (reported, investigating, contained, resolved)
    
    PATCH /api/events/{id}/ - Update only the status field
    """
    queryset = Event.objects.select_related('farm__district').all()
    serializer_class = EventSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by district code
        district_code = self.request.query_params.get('district', None)
        if district_code:
            queryset = queryset.filter(farm__district__code=district_code)
        
        # Filter by event_type
        event_type = self.request.query_params.get('event_type', None)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def partial_update(self, request, *args, **kwargs):
        """
        PATCH endpoint - only allow updating the status field
        """
        # Only allow 'status' field in PATCH
        if set(request.data.keys()) - {'status'}:
            return Response(
                {"error": "Only 'status' field can be updated via PATCH"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().partial_update(request, *args, **kwargs)
