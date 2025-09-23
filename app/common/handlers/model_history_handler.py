from django.db.models import Model
from django.db.models.fields.related import ForeignKey, ManyToManyField


class ModelHistoryHandler:
    def __init__(self, model_object: Model, history_model_class: Model, reference_field: str = "back_reference",
                 fields_to_skip_on_update: list = []):
        self.model_object = model_object
        self.history_model_class = history_model_class
        self.reference_field = reference_field
        self.fields_to_skip_on_update = fields_to_skip_on_update

    def create_history(self):
        model_fields = self.model_object._meta._get_fields(forward=True, reverse=False)

        history_model_class_fields = [history_model_field.name for history_model_field in
                                      self.history_model_class._meta._get_fields(forward=True, reverse=False)]

        fields_to_not_migrate = ["id"]
        if self.fields_to_skip_on_update:
            fields_to_not_migrate += self.fields_to_skip_on_update

        history_model = self.history_model_class()
        for field in model_fields:
            field_type = type(field)
            field_name = field.name
            if field_name in history_model_class_fields and field_name not in fields_to_not_migrate:
                if field_type == ManyToManyField:
                    continue

                model_value = getattr(self.model_object, field_name)
                setattr(history_model, field_name, model_value)

        setattr(history_model, self.reference_field, self.model_object)
        history_model.save()

        many_to_many_model_fields = self.model_object._meta.many_to_many
        history_model_class_many_to_many_fields = [history_model_field.name for history_model_field in
                                                   self.history_model_class._meta.many_to_many]

        for many_to_many_field in many_to_many_model_fields:
            field_name = many_to_many_field.name
            if field_name in history_model_class_many_to_many_fields:
                many_to_many_objects = getattr(self.model_object, field_name).all()

                for obj in many_to_many_objects:
                    getattr(history_model, field_name).add(obj)

        return history_model




