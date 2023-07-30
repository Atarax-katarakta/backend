from django.db import models

# Create your models here.


class City(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Speciality(models.Model):
    title = models.CharField(max_length=128)
    code = models.CharField(max_length=8, primary_key=True, unique=True)
    description = models.TextField()
    education_level = models.CharField(max_length=16)


class University(models.Model):
    title = models.CharField(max_length=128)
    link = models.URLField()
    grade = models.CharField(max_length=20)
    image = models.URLField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    speciality = models.ManyToManyField(Speciality, through='UniversitySpeciality')


class UniversitySpeciality(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    budget_places = models.IntegerField()
    contract_places = models.IntegerField()
    budget_passing_score = models.IntegerField()
    contract_passing_score = models.IntegerField()
    price = models.IntegerField()


class Bank(models.Model):
    title = models.CharField(max_length=64)
    logo = models.ImageField(upload_to='images/banks/')
    link = models.URLField()


class BankService(models.Model):
    title = models.CharField(max_length=64)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    description = models.TextField()
    min_percent = models.FloatField()
    max_percent = models.FloatField()
    default_price = models.FloatField(null=True, blank=True)
    # link_on_service_api = models.URLField()
    # settings = models.JSONField()


class PeopleBankService(models.Model):
    user_id = models.BigIntegerField()
    service = models.ForeignKey(BankService, on_delete=models.PROTECT)
    approved = models.BooleanField(default=False, blank=True)


class UniversityApprove(models.Model):
    user_id = models.BigIntegerField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False, blank=True)
