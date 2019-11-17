from rest_framework import serializers
from .models import LNMOnline

class LNMOnlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = LNMOnline
        fields = ['id']
