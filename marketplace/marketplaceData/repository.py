from .models import *


class CityRepository:

    @staticmethod
    def get_queryset():
        return City.objects.all()

    @staticmethod
    def get_or_create_city_by_name(name: str):
        city, created = City.objects.get_or_create(title=name)
        return city


class UniversityRepository:

    @staticmethod
    def get_queryset():
        return University.objects.all()

    @staticmethod
    def add_university(title: str, link: str, grade: str, city: str, image: str):
        return University.objects.create(
            title=title,
            link=link,
            grade=grade,
            city=CityRepository.get_or_create_city_by_name(city),
            image=image
        )

    @staticmethod
    def get_university_by_city(city_name: str):
        return University.objects.filter(city=City.objects.get(title=city_name))


class BankRepository:

    @staticmethod
    def get_queryset():
        return Bank.objects.all()


class BankServiceRepository:

    @staticmethod
    def get_queryset():
        return BankService.objects.all()

    @staticmethod
    def get_by_id(pk: int):
        return BankService.objects.get(pk=pk)


class SpecialityRepository:

    @staticmethod
    def get_queryset():
        return Speciality.objects.all()

    @staticmethod
    def add_speciality(code: str, title: str, description: str, education_level: str):
        speciality, created = Speciality.objects.get_or_create(
            code=code,
            title=title,
            description=description,
            education_level=education_level
        )
        return speciality


class UniversitySpecialityRepository:

    @staticmethod
    def get_queryset():
        return UniversitySpeciality.objects.all()

    @staticmethod
    def get_by_id(pk: int):
        return UniversitySpeciality.objects.get(pk=pk)

    @staticmethod
    def get_filtered_by_speciality(speciality_id: str):
        return UniversitySpeciality.objects.filter(speciality__code=speciality_id)

    @staticmethod
    def get_filtered_by_university(university_id: int):
        return UniversitySpeciality.objects.filter(university=University.objects.get(pk=university_id))

    @staticmethod
    def add_university_speciality(university: University, speciality: Speciality, budget_places: int, contract_places,
                                  budget_passing_score: int, contract_passing_score: int, price: float):
        return UniversitySpeciality.objects.create(
            university=university,
            speciality=speciality,
            budget_places=budget_places,
            contract_places=contract_places,
            budget_passing_score=budget_passing_score,
            contract_passing_score=contract_passing_score,
            price=price
        )


class PeopleBankServiceRepository:

    @staticmethod
    def get_queryset(user_id):
        return PeopleBankService.objects.filter(user_id=user_id)

    @staticmethod
    def add_service(user_id: int, service_id: int, approved: bool = False):
        return PeopleBankService.objects.create(
            user_id=user_id,
            service_id=service_id,
            approved=approved
        )


class UniversityApproveRepository:

    @staticmethod
    def get_queryset():
        return UniversityApprove.objects.all()

    @staticmethod
    def add_ticket(user_id: int, university: University, approved: bool = False):
        return PeopleBankService.objects.create(
            user_id=user_id,
            university=university,
            approved=approved
        )