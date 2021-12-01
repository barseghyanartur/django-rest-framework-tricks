from django.apps import AppConfig

__all__ = ("Config",)


class Config(AppConfig):
    """Config."""

    name = "books"
    label = "books"
