from django.contrib import admin
from .models import topic_ofinterest, Entry
# Register your models here.
admin.site.register(topic_ofinterest) #in the admin site, it will show there.
admin.site.register(Entry) #in the admin site, it will show there.