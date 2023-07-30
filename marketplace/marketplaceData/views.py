from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Response
from rest_framework.viewsets import ModelViewSet

from .repository import *
from .serializers import *
from .services import *
from .tasks import get_university_and_specialitites_data_from_json

# Create your views here.


class CityViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer
    queryset = CityRepository.get_queryset()


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


class UniversitySpecialityFilteredAPIView(ListAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = UniversitySpecialitySerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'university_id',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='id универа',
                required=True,
            ),
        ]
    )
    def get_queryset(self):
        return UniversitySpecialityRepository.get_filtered_by_university(self.request.query_params.get('university_id'))


class GetUniversityByCityListAPIView(ListAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = UniversitySoloSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'city_name',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='название города',
                required=True,
            ),
        ]
    )
    def get_queryset(self):
        return UniversityRepository.get_university_by_city(self.request.query_params.get('city_name'))


class AddUniversitySpecialityAPIView(APIView):

    def post(self, request):
        get_university_and_specialitites_data_from_json.apply_async((request.data,))
        return Response(status=status.HTTP_200_OK)


class PeopleBankingServiceAPIView(ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = PeopleBankServiceSerializer

    def get_queryset(self):
        return PeopleBankServiceRepository.get_queryset(self.request.query_params['user_id'])

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя'),
            'bank_service_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID услуги банка в БД'),
            'passport': openapi.Schema(type=openapi.TYPE_STRING, description='серия и номер паспорта'),
            'university_speciality_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                       description='ID записи из БД, где нужное направление и универ'),
            'months': openapi.Schema(type=openapi.TYPE_INTEGER, description='кол-во месяцев, на сколько кредит')
        },
        required=['university_speciality_id', 'bank_service_id', 'user_id', 'passport', 'months']
    ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'approved': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        approved = prove_bank(request.data['passport'], UniversitySpecialityRepository.get_by_id(
            request.data['university_speciality_id']).price, BankServiceRepository.get_by_id(
            request.data['bank_service_id']).max_percent, request.data['percent'])
        if approved:
            payment()
        return Response(data={'approved': approved}, status=status.HTTP_201_CREATED)


class UniversityApproveAPIView(ListCreateAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = (AllowAny,)
    serializer_class = UniversityApproveSerializer

    def get_queryset(self):
        pass

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя'),
            'university_speciality_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                       description='ID записи из БД, где нужное направление и универ'),
            'student_ege': openapi.Schema(type=openapi.TYPE_INTEGER, description='сумма баллов абитуриента по ЕГЭ')
        },
        required=['university_speciality_id', 'student_ege', 'user_id']
    ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'approved': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            ),
        }
    )
    def create(self, request, *args, **kwargs):
        approved = prove_university(UniversitySpecialityRepository.get_by_id(
            request.data['university_speciality_id']).contract_passing_score, request.data['student_ege'])
        UniversityApproveRepository.add_ticket(
            user_id=request.data['user_id'],
            university=UniversitySpecialityRepository.get_by_id(request.data['university_speciality_id']).university,
            approved=approved
        )
        return Response(data={'approved': approved}, status=status.HTTP_201_CREATED)
