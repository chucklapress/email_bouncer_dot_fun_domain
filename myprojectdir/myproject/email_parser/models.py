from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class dmarc_check(models.Model):
    address = models.CharField(max_length=120)
    domain = models.CharField(max_length=30)
    subject = models.CharField(max_length=120)
    the_dmarc_record = models.CharField(max_length=360)
    time_parsed = models.CharField(max_length=120)
    return_from = models.CharField(max_length=120)
    def __str__(self):
        return self.address
