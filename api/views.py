from django.db.models.aggregates import Sum, Max
from django.db.models.functions.datetime import ExtractYear, ExtractMonth
from django.db.models import Max

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import StationSerializer
from .models import Station, DailyCounts2021, DailyCounts2020, DailyCounts2019

from update.tasks import WeeklyUpdate

@api_view(['GET'])
def index(request):
    content = {
        "endpoints": {
            "stations": {
                "GET": "returns list of all stations with coordinates and other descriptors"
            },
            "month/:year": {
                "GET": "returns list of each station with the total number of entries and exits over the entire month of the requested year"
            },
            "year/:year": {
                "GET": "returns list of each station with the total number of entries and exits over the entire requested year"
            },
            "totals": {
                "GET": "returns aggregate information including single day max entry and exit values for each year"
            }
        }
    }
    return Response(content)

@api_view(['GET'])
def stations(request):
    # Trigger the update task
    WeeklyUpdate.apply_async()
    
    stations = Station.objects.all().order_by('stop_name')
    serializer = StationSerializer(stations, many=True)

    return Response(serializer.data)

class Yearly2021View(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        entries = DailyCounts2021.objects.annotate(year=ExtractYear('date')).values(
        'stop_name',
        'daytime_routes',
        'gtfs_latitude',
        'gtfs_longitude',
        'year'
        ).annotate(total_year_entries=Sum('entries')).annotate(total_year_exits=Sum('exits')).order_by('stop_name')
                
        return Response(entries)

class Yearly2020View(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        entries = DailyCounts2020.objects.annotate(year=ExtractYear('date')).values(
        'stop_name',
        'daytime_routes',
        'gtfs_latitude',
        'gtfs_longitude',
        'year'
        ).annotate(total_year_entries=Sum('entries')).annotate(total_year_exits=Sum('exits')).order_by('stop_name')
                
        return Response(entries)

class Yearly2019View(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        entries = DailyCounts2019.objects.annotate(year=ExtractYear('date')).values(
        'stop_name',
        'daytime_routes',
        'gtfs_latitude',
        'gtfs_longitude',
        'year'
        ).annotate(total_year_entries=Sum('entries')).annotate(total_year_exits=Sum('exits')).order_by('stop_name')
                
        return Response(entries)
        

class Monthly2019View(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        entries = DailyCounts2019.objects\
            .annotate(month=ExtractMonth('date'))\
                .values(
                    'stop_name',
                    'daytime_routes',
                    'gtfs_latitude',
                    'gtfs_longitude',
                    'month')\
                    .annotate(monthly_entries=Sum('entries'), monthly_exits=Sum('exits'))\
                    .order_by('stop_name')\
                    
        return Response(entries)

class Monthly2020View(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        entries = DailyCounts2020.objects\
            .annotate(month=ExtractMonth('date'))\
                .values(
                    'stop_name',
                    'daytime_routes',
                    'gtfs_latitude',
                    'gtfs_longitude',
                    'month')\
                    .annotate(monthly_entries=Sum('entries'), monthly_exits=Sum('exits'))\
                    .order_by('stop_name')\
                    
        return Response(entries)

class Monthly2021View(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        entries = DailyCounts2021.objects\
            .annotate(month=ExtractMonth('date'))\
                .values(
                    'stop_name',
                    'daytime_routes',
                    'gtfs_latitude',
                    'gtfs_longitude',
                    'month')\
                    .annotate(monthly_entries=Sum('entries'), monthly_exits=Sum('exits'))\
                    .order_by('stop_name')\
                    
        return Response(entries)
    

class AggregateView(APIView):
    
    def get(self, request, format=None):
        entries19 = DailyCounts2019.objects.aggregate(Max('entries'))
        exits19 = DailyCounts2019.objects.aggregate(Max('exits'))
            
        entries20 = DailyCounts2020.objects.aggregate(Max('entries'))
        exits20 = DailyCounts2020.objects.aggregate(Max('exits'))
            
        entries21 = DailyCounts2021.objects.aggregate(Max('entries'))
        exits21 = DailyCounts2021.objects.aggregate(Max('exits'))

        content = {
            'entries': {
                '2021': entries21,
                '2020': entries20,
                '2019': entries19,
            },
            'exits': {
                '2021': exits21,
                '2020': exits20,
                '2019': exits19,
            }
        }

        return Response(content)
