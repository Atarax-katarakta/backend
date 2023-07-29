from rest_framework import serializers
from .models import *


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'


class SpecialitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Speciality
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('title',)


class UniversitySerializer(serializers.ModelSerializer):
    speciality = SpecialitySerializer(
        many=True,
        read_only=True
    )
    city = serializers.StringRelatedField()

    class Meta:
        model = University
        fields = ('link', 'title', 'grade', 'image', 'city', 'speciality')


class BankServiceSerializer(serializers.ModelSerializer):
    bank = BankSerializer()

    class Meta:
        model = BankService
        fields = '__all__'


class UniversitySoloSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = University
        fields = ('link', 'title', 'grade', 'city', 'image')


class UniversitySpecialitySerializer(serializers.ModelSerializer):
    university = UniversitySoloSerializer()
    speciality = SpecialitySerializer()

    class Meta:
        model = UniversitySpeciality
        fields = '__all__'
