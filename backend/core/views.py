from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from django.db.models import Q, Count, Sum
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
        "message": "Акыл Жер Government Portal API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health/",
            "districts": "/api/districts/",
            "farms": "/api/farms/",
            "events": "/api/events/",
            "dashboard": "/api/dashboard/summary/",
            "admin": "/admin/"
        }
    })


@api_view(['GET'])
def dashboard_summary(request):
    """
    Dashboard summary statistics
    
    Query Parameters:
    - district: Filter by district code (optional)
    """
    district_code = request.query_params.get('district', None)
    
    # Base querysets
    farms_qs = Farm.objects.all()
    herds_qs = Herd.objects.all()
    events_qs = Event.objects.all()
    
    # Apply district filter if provided
    if district_code:
        farms_qs = farms_qs.filter(district__code=district_code)
        herds_qs = herds_qs.filter(farm__district__code=district_code)
        events_qs = events_qs.filter(farm__district__code=district_code)
    
    # Total farms
    total_farms = farms_qs.count()
    
    # Total animals (sum of all herd headcounts)
    total_animals = herds_qs.aggregate(total=Sum('headcount'))['total'] or 0
    
    # Open outbreaks (disease_report or mortality with status new/in_progress)
    open_outbreaks = events_qs.filter(
        event_type__in=['disease_report', 'mortality'],
        status__in=['new', 'in_progress']
    ).count()
    
    # Farms by district
    if district_code:
        # If filtering by district, only show that district
        farms_by_district = farms_qs.values(
            'district__code', 'district__name'
        ).annotate(
            farm_count=Count('id')
        ).order_by('district__name')
    else:
        # Show all districts
        farms_by_district = Farm.objects.values(
            'district__code', 'district__name'
        ).annotate(
            farm_count=Count('id')
        ).order_by('district__name')
    
    farms_by_district_list = [
        {
            'district_code': item['district__code'],
            'district_name': item['district__name'],
            'farm_count': item['farm_count']
        }
        for item in farms_by_district
    ]
    
    # Outbreaks by disease (for disease_report/mortality where disease_suspected is not null)
    outbreaks_by_disease = events_qs.filter(
        event_type__in=['disease_report', 'mortality'],
        disease_suspected__isnull=False
    ).values('disease_suspected').annotate(
        count=Count('id')
    ).order_by('-count')
    
    outbreaks_by_disease_list = [
        {
            'disease_suspected': item['disease_suspected'],
            'count': item['count']
        }
        for item in outbreaks_by_disease
    ]
    
    return Response({
        'total_farms': total_farms,
        'total_animals': total_animals,
        'open_outbreaks': open_outbreaks,
        'farms_by_district': farms_by_district_list,
        'outbreaks_by_disease': outbreaks_by_disease_list
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
