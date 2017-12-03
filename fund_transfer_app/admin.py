from django.contrib import admin
from .models import Node, Transaction

# Register your models here.
admin.site.register(Node)
admin.site.register(Transaction)