from rest_framework import serializers
from .models import Calculation

class calculateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Calculation
        fields = '__all__'