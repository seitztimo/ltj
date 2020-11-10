import factory

from hmac_auth.models import HMACGroup


class HMACGroupFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("text", max_nb_chars=50)

    class Meta:
        model = HMACGroup
