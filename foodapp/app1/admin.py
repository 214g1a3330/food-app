from django.contrib import admin
from app1.models import *

# Register your models here.

admin.site.register(Fooditem)
admin.site.register(Cart)
admin.site.register(Order)