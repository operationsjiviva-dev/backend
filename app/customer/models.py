from django.db import models

# Create your models here.
from common.models import TimeStampedModel
import uuid


class Customer(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=56, default='')
    address = models.CharField(max_length=512, blank=True, null=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=10, default='')


class Otp(TimeStampedModel):
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    otp = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=255, default='VALID')
    role = models.CharField(max_length=255, blank=True, null=True)
    client_code = models.CharField(max_length=255, blank=True, null=True)

