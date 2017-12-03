from django.views.generic import ListView
from .models import Node

class HomePageView(ListView):
    model = Node
    template_name = 'home.html'
