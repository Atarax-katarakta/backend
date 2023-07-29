from .models import Bank, BankService, University, Speciality, UniversitySpeciality


class UniversityRepository:

    @staticmethod
    def get_queryset():
        return University.objects.all()

    @staticmethod
    def add_university(title: str, link: str, grade: str):
        return University.objects.create(
            title=title,
            link=link,
            grade=grade
        )


class BankRepository:

    @staticmethod
    def get_queryset():
        return Bank.objects.all()


class BankServiceRepository:

    @staticmethod
    def get_queryset():
        return BankService.objects.all()


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
    def get_filtered_by_speciality(speciality_id: int):
        return UniversitySpeciality.objects.filter(speciality__code=speciality_id)

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
