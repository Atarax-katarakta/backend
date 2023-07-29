import json
from typing import Dict, List
import requests
from marketplace.celery import app
from .repository import UniversityRepository, SpecialityRepository, UniversitySpecialityRepository


def find_speciality(pk: str, specialities: List[Dict]):
    return list(filter(lambda x: x['id'] == pk, specialities))[0]


@app.task
def get_university_and_specialitites_data_from_json(data):
    # print(filepath)
    # with open(filepath, 'r', encoding='UTF-8') as f:
    #     universities = json.load(f).get('universities')
    universities = data.get('universities')
    for university in universities:
        university_object = UniversityRepository.add_university(
            title=university['title'],
            link=university['site'],
            grade=university['grade']
        )
        try:
            for speciality in university.get("specialities"):
                speciality_object = SpecialityRepository.add_speciality(
                    code=speciality['code'],
                    title=speciality['title'],
                    description=speciality['description'],
                    education_level=speciality['education_level']
                )
                university_speciality = UniversitySpecialityRepository.add_university_speciality(
                    university=university_object,
                    speciality=speciality_object,
                    budget_places=speciality["budget_places"],
                    contract_places=speciality["contract_places"],
                    budget_passing_score=speciality["budget_passing_score"],
                    contract_passing_score=speciality["contract_passing_score"],
                    price=speciality["price"]
                )
        except Exception:
            pass

