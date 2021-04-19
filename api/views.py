from datetime import timedelta
from api.data.importCSV import importCSV
from api.data.update import updateValues
from api.data.shouldUpdate import shouldUpdate
from django.db.models.aggregates import Sum, Max
from django.db.models.functions.datetime import ExtractYear, ExtractMonth
from django.db.models import Max

from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import StationSerializer
from .models import Station, DailyCounts2021, DailyCounts2020, DailyCounts2019

@api_view(['GET'])
def index(request):
    return Response('API BASE POINT')

@api_view(['GET'])
def stations(request):
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

class WeeklyUpdateView(APIView):
    
    def get(self, request, format=None):
        
        today = '210327'
        upToDate = shouldUpdate()
        if "error" in upToDate:
            return Response({'success': False, 'error': upToDate["error"]})

        if(upToDate["shouldUpdate"] == False):
            return Response({'success': True, 'message': "All records are up to date"})
        
        print("db most recent saturday: " + upToDate["dbMostRecentSaturday"].strftime("%Y-%m-%d"))
        print("current saturday: " + upToDate["currentSaturday"].strftime("%Y-%m-%d"))

        saturdayToImport = upToDate["dbMostRecentSaturday"] + timedelta(days=7) 
        currentSaturday = upToDate["currentSaturday"]

        # download and import new weekly data
        while(saturdayToImport <= currentSaturday):
            result = importCSV(DATE=saturdayToImport.strftime("%y%m%d"))
            if(result['success'] == False):
                content = {
                    'success': result['success'],
                    'error': result['error']
                }
                return Response(content, status=result['status'])   
            saturdayToImport = saturdayToImport + timedelta(days=7)  

        # update net values
        result = updateValues(year = upToDate["dbMostRecentSaturday"].year)
        content = {
            'success': result['success'],
            'error': result['error']
        }

        return Response(content, status=result['status'])

