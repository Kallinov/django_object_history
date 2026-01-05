class TrackedModelMixin:

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        from django.db.models.signals import pre_delete, post_save, pre_save

        pre_save.connect(cls._pre_save_handler, sender=cls)
        post_save.connect(cls._post_save_handler, sender=cls)
        pre_delete.connect(cls._pre_delete_handler, sender=cls)
        
    @staticmethod
    def _pre_save_handler(sender, instance, **kwargs):
        created = instance._state.adding

        if not created:
            instance._old_instance = sender.objects.get(pk=instance.pk)

    @staticmethod
    def _post_save_handler(sender, instance, created, update_fields, **kwargs):
        from .models import HistoryEntry, ContentType

        changes = dict()

        if not created:
            ignored_fields = ['created_at', 'updated_at']
            old_instance = getattr(instance, '_old_instance', None)

            for field in instance._meta.fields:
                name = field.name

                if name in ignored_fields:
                    continue

                old_value = getattr(old_instance, name, None)
                new_value = getattr(instance, name, None)

                if old_value != new_value:
                    changes[name] = {
                            'old_value': old_value,
                            'new_value': new_value
                        }

        action = 'c' if created else 'u'
        
        h = HistoryEntry(
        content_type=ContentType.objects.get_for_model(instance.__class__),
        object_id=instance.id,
        object_repr=str(instance),
        action=action,
        changed_by=getattr(instance, '_history_user', None),
        changes=changes
        )
        h.save()


    @staticmethod
    def _pre_delete_handler(sender, instance, **kwargs):
        from .models import HistoryEntry, ContentType
        
        h = HistoryEntry(
        content_type=ContentType.objects.get_for_model(instance.__class__),
        object_id=instance.id,
        object_repr=str(instance),
        action='d',
        changed_by=getattr(instance, '_history_user', None),
        changes={}
        )
        h.save()