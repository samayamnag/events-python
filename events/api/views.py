from django.shortcuts import render
from events.models import Event
from rest_framework import generics
from events.api.serializers import EventCreateSerializer
from rest_framework.response import Response
from events.utils import get_client_ip
from rest_framework.exceptions import NotAuthenticated,NotFound
from rest_framework.reverse import reverse
from rest_framework import status
from events.decorators import LoginRequiredMixin
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from django.core.files.storage import FileSystemStorage
import uuid


class CreateEvent(generics.CreateAPIView):
    serializer_class = EventCreateSerializer
    queryset = Event.objects.all()
    parser_classes = (MultiPartParser, FormParser,FileUploadParser)

    def perform_create(self, serializer):
        myfile = self.request.data.get('banner')
        fs = FileSystemStorage()
        filename = fs.save('images/'+str(uuid.uuid4()) + '_' + myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        
        if serializer.is_valid():
            serializer.save(ip_address=get_client_ip(self.request), banner=uploaded_file_url)
            serializer_data = serializer.data
            data = {
                'id': serializer_data['id']
            }
            return Response(data, status=201)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    serializer_class = EventCreateSerializer
    queryset = Event.objects.all()

    def retrieve(self, request, *args, **kwargs):
        if hasattr(request, 'auth_user'):
            auth_user = request.auth_user       
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            data['coordinates'] = instance.coordinates
            data['url'] = 'http://events.ichangemycity.com/' + str(instance.id)
            data['web_url'] = 'http://events.ichangemycity.com/events/' + str(instance.id)
            data['created_by'] = auth_user['id']
            data['banner'] = instance.banner

            return Response(data)
        
        return Response({'message': 'Unauthenticated'}, status=401)

