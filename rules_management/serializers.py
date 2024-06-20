# serializers.py
from rest_framework import serializers
from .models import Rule

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        
class RuleSequenceUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    currentIndex = serializers.IntegerField()