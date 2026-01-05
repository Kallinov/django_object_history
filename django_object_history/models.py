from django.db import models
from django.contrib.contenttypes.models import ContentType
from .enums import OperationType
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .mixins import TrackedModelMixin

valid_operations = [choice[0] for choice in OperationType.choices]

class HistoryEntry(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    object_repr = models.CharField()
    action = models.CharField(choices=OperationType.choices)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now=True)
    changes = models.JSONField(blank=True, null=True)

    def clean(self): # Python-level validation
        if self.action not in valid_operations:
            raise ValidationError(
                f"""
                "{self.action}" is not a valid action.
                Valid actions are: {valid_operations}"""
            )
        return super().clean()
    
    def full_clean(self):
        self.clean()
        return super().full_clean()
    
    class Meta: # Database-level validation
        constraints = [
            models.CheckConstraint(
                condition=models.Q(action__in=valid_operations),
                name=f"""Action validation. Valid actions are: {valid_operations}."""
            )
        ]

    