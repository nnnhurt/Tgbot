"""Module apps for app."""
from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    App configuration class for the 'app' application.

    Attributes:
        default_auto_field (str): The default primary key
        type for models in the app.
        name (str): The name of the app.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
