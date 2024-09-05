from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from apps.main.models import Species, Fish


class TestAddFish(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.species = Species.objects.create(name='a', base=Decimal('15.122'))
        self.species2 = Species.objects.create(name='b', base=Decimal('7.561'))

    def test_add_fish(self):
        fish = Fish.objects.create(weight=Decimal('15.122'), user=self.user, species=self.species)
        self.assertEqual(fish.points, 100)

        fish2 = Fish.objects.create(weight=Decimal('7.561'), user=self.user, species=self.species)
        self.assertEqual(fish2.points, 50)

        fish = Fish.objects.get(pk=fish.pk)
        self.assertEqual(fish.points, 100)  # biggest fish points should not be altered

        fish3 = Fish.objects.create(weight=Decimal('30.244'), user=self.user, species=self.species)
        self.assertEqual(fish3.points, 100)

        fish = Fish.objects.get(pk=fish.pk)
        self.assertEqual(fish.points, 50)  # smaller fish points should be altered

        fish2 = Fish.objects.get(pk=fish2.pk)
        self.assertEqual(fish2.points, 25)  # smaller fish points should be altered

        with self.assertNumQueries(3):
            Fish.objects.create(weight=Decimal('50'), user=self.user, species=self.species)
