from rest_framework_mongoengine import serializers as mongoserializers

from events.models import Event, Channel
from rest_framework import serializers
import datetime
from events.utils import get_client_ip, Ward


class EventCreateSerializer(mongoserializers.DocumentSerializer):
    
    id = serializers.CharField(max_length=255, read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
    landmark = serializers.CharField(max_length=255)
    latitude = serializers.CharField(max_length=50, write_only=True)
    longitude = serializers.CharField(max_length=50, write_only=True)
    start_timestamp = serializers.DateTimeField(default=datetime.datetime.now)
    end_timestamp = serializers.DateTimeField(default=datetime.datetime.now)
    tags = serializers.ListField(default=None)
    channel = serializers.CharField()
    city = serializers.CharField(max_length=100, read_only=True)
    banner = serializers.ImageField(max_length=None, use_url=True)
    

    class Meta:
        model = Event
        #fields = '__all__'
        fields = ('id','title', 'description', 'location', 'recurring',
        'open_event', 'start_timestamp', 'end_timestamp', 'tags', 'banner', 'channel', 'landmark',
        'latitude', 'longitude', 'city')
        #read_only_fields = ('slug',)
        #write_only_fields = ('channel_slug', )

    def create(self, validated_data):
        input_channel = validated_data['channel']
        channel = Channel.objects(slug=input_channel).first()
        latitude = validated_data['latitude']
        longitude = validated_data['longitude']
        validated_data['channel'] = channel.id
        validated_data['coordinates'] = [float(latitude), 
        float(latitude)]
        validated_data['tags'] = ['tag1']
        validated_data['created_by'] = 1

        ward = Ward().get_by_geo_location(latitude,longitude)

        validated_data['city'] = ward['city_name'] or None

        # Remove latitude and longitude
        del validated_data["latitude"]
        del validated_data['longitude']

        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        latitude = validated_data['latitude']
        longitude = validated_data['longitude']
        validated_data['coordinates'] = [float(latitude), 
        float(latitude)]
        validated_data['tags'] = ['tag1']

        ward = Ward().get_by_geo_location(latitude,longitude)

        validated_data['city'] = ward['city_name'] or None

        # Remove latitude and longitude
        del validated_data["latitude"]
        del validated_data['longitude']

        instance.save()

        return instance

        