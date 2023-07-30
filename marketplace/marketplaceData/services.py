from django.conf import settings
import requests


def prove_university(minimal_ege: int, student_ege: int):
    return requests.get(settings.UNIVERSITY_EXAMPLE_API + 'educational_approve', params={
        'minimal_ege': minimal_ege,
        'student_ege': student_ege
    }).json().get('answer')


def prove_bank(passport: str, summary: int, percent: float, months: int):
    return requests.get(settings.BANK_EXAMPLE_API + 'credit/', params={
        'passport': passport,
        'summary': summary,
        'percent': percent,
        'months': months
    }).json().get('answer') == 'yes'


def payment():
    return requests.post(settings.UNIVERSITY_EXAMPLE_API + 'payment').json().get('answer')

