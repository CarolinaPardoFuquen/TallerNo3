from django.contrib.auth.models import User
from .models import Recomendations, RecomendationsCat

import django_filters

class RecomendationsFilter(django_filters.FilterSet):
    class Meta:
        model = Recomendations
        fields = ['ID_User']
    

