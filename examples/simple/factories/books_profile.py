import random

from factory import DjangoModelFactory, LazyAttribute

from books.models import Profile

from .factory_faker import Faker

__all__ = (
    'ProfileFactory',
    'LimitedProfileFactory',
    'SingleProfileFactory',
)


class BaseProfileFactory(DjangoModelFactory):
    """Base author factory."""

    salutation = Faker('text', max_nb_chars=10)
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    birth_date = Faker('date')
    biography = Faker('text')
    phone_number = Faker('phone_number')
    website = Faker('url')
    company = Faker('company')
    company_phone_number = Faker('phone_number')
    company_email = Faker('email')
    company_website = Faker('url')
    bank_name = Faker('company')
    bank_account_name = Faker('name')
    bank_account_number = Faker('pystr')

    class Meta(object):
        """Meta class."""

        model = Profile
        abstract = True


class ProfileFactory(BaseProfileFactory):
    """Profile factory."""


class LimitedProfileFactory(BaseProfileFactory):
    """Profile factory, but limited to 20 profiles."""

    id = LazyAttribute(
        lambda __x: random.randint(1, 20)
    )

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('id',)


class SingleProfileFactory(BaseProfileFactory):
    """Profile factory, limited to a single profile."""

    id = 999999
    name = "Artur Barseghyan"
    email = "barseghyan@gw20e.com"

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('id',)
