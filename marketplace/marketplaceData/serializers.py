from rest_framework import serializers
from .models import *


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):

    class Meta:
        model = University
        fields = '__all__'


class SpecialitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Speciality
        fields = '__all__'


class BankServiceSerializer(serializers.ModelSerializer):
    bank = BankSerializer()

    class Meta:
        model = BankService
        fields = '__all__'


class UniversitySpecialitySerializer(serializers.ModelSerializer):
    university = UniversitySerializer()
    speciality = SpecialitySerializer()

    class Meta:
        model = UniversitySpeciality
        fields = '__all__'
