from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BankViewSet, BankServiceViewSet, UniversityViewSet, UniversitySpecialityViewSet, UniversitySpecialityFilteredListAPIView, SpecialityViewSet, AddUniversitySpecialityAPIView


router = DefaultRouter()
router.register(r'banks', BankViewSet, 'bank')
router.register(r'bankServices', BankServiceViewSet, 'bankService')
router.register(r'universities', UniversityViewSet, 'university')
router.register(r'specialities', SpecialityViewSet, 'speciality')
router.register(r'universitySpecialities', UniversitySpecialityViewSet, 'universitySpeciality')
urlpatterns = [
    path('filteredspecialities/', UniversitySpecialityFilteredListAPIView.as_view()),
    path('upload/', AddUniversitySpecialityAPIView.as_view())
]
urlpatterns += router.urls
