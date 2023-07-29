from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet

from .repository import BankRepository, SpecialityRepository, UniversitySpecialityRepository, BankServiceRepository, UniversityRepository
from .serializers import BankSerializer, BankServiceSerializer, UniversitySerializer, SpecialitySerializer, UniversitySpecialitySerializer
from .tasks import get_university_and_specialitites_data_from_json

# Create your views here.


class BankViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = BankSerializer
    queryset = BankRepository.get_queryset()


class UniversityViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = UniversitySerializer
    queryset = UniversityRepository.get_queryset()


class SpecialityViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = SpecialitySerializer
    queryset = SpecialityRepository.get_queryset()


class BankServiceViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = BankServiceSerializer
    queryset = BankServiceRepository.get_queryset()


class UniversitySpecialityViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = UniversitySpecialitySerializer
    queryset = UniversitySpecialityRepository.get_queryset()


class UniversitySpecialityFilteredListAPIView(ListAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = UniversitySpecialitySerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'speciality_code',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='код специальности, прям так и передаём строкой с точечками',
                required=True,
            ),
        ]
    )
    def get_queryset(self):
        return UniversitySpecialityRepository.get_filtered_by_speciality(self.request.query_params.get('speciality_code'))


class AddUniversitySpecialityAPIView(APIView):

    def post(self, request):
        get_university_and_specialitites_data_from_json.apply_async((request.data,))
        return Response(status=status.HTTP_200_OK)
