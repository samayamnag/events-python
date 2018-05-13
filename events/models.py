from django_mongoengine import Document, EmbeddedDocument
from django_mongoengine import fields
import datetime
from mongoengine.signals import pre_save
from django.utils.text import slugify
from .utils import get_client_ip


class Event(Document):
    title = fields.StringField(max_length=255)
    description = fields.StringField(max_length=255)
    location = fields.StringField(max_length=255)
    landmark = fields.StringField(max_length=255)
    city = fields.StringField(max_length=255)
    coordinates = fields.ListField(fields.FloatField())
    start_timestamp = fields.DateTimeField()
    end_timestamp = fields.DateTimeField()
    banner = fields.StringField()
    #banner = fields.ImageField(upload_to='banners', default="images/None/no-img.jpeg")
    #banner = fields.ImageField(upload_to=fs, default="images/None/no-img.jpeg")  
    tags = fields.ListField(fields.StringField())
    recurring = fields.BooleanField(default=False)
    open_event = fields.BooleanField(default=True)
    full_day_event = fields.BooleanField(default=False)
    created_by = fields.IntField()
    user_agent = fields.StringField(blank=True)
    timestamp = fields.DateTimeField(default=datetime.datetime.now)
    updated_at = fields.DateTimeField(default=datetime.datetime.now)
    slug = fields.StringField(blank=True)
    ip_address = fields.StringField(blank=True)
    channel = fields.ObjectIdField()
    deleted = fields.BooleanField(default=False)
    deleted_at = fields.DateTimeField(blank=True)

    meta = {
        'collection': 'events'
    }

    def __str__(self):
        return self.title

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.title = document.title.capitalize()
        document.description = document.description.capitalize()
        document.location = document.location.title()
        document.landmark = document.landmark.title()
        document.city = document.city.title()

        if not document.slug:
            document.slug = slugify(document.title)


pre_save.connect(Event.pre_save, sender=Event)


class Channel(Document):
    title = fields.StringField(max_lenght=100, blank=False)
    slug = fields.StringField(max_lenght=150, blank=False)
    platform = fields.StringField(default="Swachhata", choices=['Swachhata', 'ICMYC'])
    app_name = fields.StringField(blank=False)
    type = fields.StringField(blank=False)
    archived = fields.BooleanField(default=False)
    created_at = fields.DateTimeField(default=datetime.datetime.now)
    updated_at = fields.DateTimeField()

    meta = {
        'collection': 'channels'
    }

    def __str__(self):
        return self.title

'''
from events.models import Event
from django.utils import timezone

 event = Event(created_by=21, title="test title", description="test desc", location="bangalore", landmark="near hdfc", \
 coordinates=[77.286, 12.239],  city="bangalore", start_timestamp=timezone.now(), end_timestamp=timezone.now(), \
 channel="5af1b2202e21e82c20065692",updated_at=timezone.now(), banner="banners/test.png", \
 tags=["category1", "category2"]).save()
 '''
