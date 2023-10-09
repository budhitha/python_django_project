from rest_framework import serializers
from .models import CarParts


class CarPartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarParts
        fields = '__all__'
