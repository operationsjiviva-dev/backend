from django.db import models
from django.apps import apps


class TimeStampedModel(models.Model):
    create_history_on_save = False
    history_model = None
    back_reference_field = "back_reference"
    fields_to_skip_on_update = []

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SystemSettings(TimeStampedModel):
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=1000)

    def __str__(self):
        return self.key 

