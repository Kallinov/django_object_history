from django.db import models

class OperationType(models.TextChoices):
    C = 'c', 'create'
    U = 'u', 'update'
    D = 'd', 'delete'