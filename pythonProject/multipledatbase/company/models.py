from django.db import models


# Create your models here.


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_user_name = models.CharField(max_length=100)
    company_email = models.EmailField()
    company_password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'company-details'

    def __str__(self):
        return f"{self.company_email}"


class ItemCompany(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'companyitems'
        app_label = 'company'

