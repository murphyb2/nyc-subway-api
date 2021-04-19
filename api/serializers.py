from rest_framework import serializers
from .models import Station, DailyCounts2021, DailyCounts2020, DailyCounts2019

class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station 
        fields = '__all__'

class Daily2019Serializer(serializers.ModelSerializer):

    class Meta:
        model = DailyCounts2019 
        fields = '__all__'

class Daily2020Serializer(serializers.ModelSerializer):
    month = serializers.IntegerField()
    total_entries = serializers.IntegerField()
    class Meta:
        model = DailyCounts2020 
        fields = '__all__'
        
class Daily2021Serializer(serializers.ModelSerializer):

    class Meta:
        model = DailyCounts2021 
        fields = '__all__'