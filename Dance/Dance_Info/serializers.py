from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from .models import Club, Coach, Dancer


class ClubModel:
    def __init__(self, club_name, coach):
        self.club_name = club_name
        self.coach = coach


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ("club_name", "coach", "city")


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = "__all__"


class DancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dancer
        fields = "__all__"

# class ClubSerializer (serializers.Serializer):
#     club_name = serializers.CharField(max_length=255)
#     coach_id = serializers.IntegerField()
#     city = serializers.CharField()

# def create(self, validated_data):
#     return Club.objects.create(**validated_data)
#
# def update(self, instance, validated_data):
#     instance.club_name= validated_data.get("club_name", instance.club_name)
#     instance.city = validated_data.get("city", instance.city)
#     instance.coach_id = validated_data.get("coach_id", instance.coach_id)
#     instance.save()
#     return instance


# def encode():
#     model = ClubModel('Rondo', 'Voronaya')
#     model_sr = ClubSerializer(model)
#     print(model_sr.data,type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)

