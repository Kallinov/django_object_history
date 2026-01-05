# django-object-history

django-object-history is a Django app that allows you
to see the history of object changes.


Quick start
-----------

1. Add "history" to your INSTALLED_APPS setting like this:
    ```
    INSTALLED_APPS = [
        ...,
        "django_profiles.apps.DjangoObjectHistoryConfig",
    ]
    ```

3. Run ```python manage.py migrate``` to create the models.

4. To be able to see the history of an object, make it a subclass of the TrackedModelMixin like this:
   ```
   class MyClass(TrackedModelMixin, models.Model): ...
   ```
