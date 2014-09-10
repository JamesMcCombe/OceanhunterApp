from django.db import models
from django.contrib.auth.models import User

class Species(models.Model):
    class Meta:
        verbose_name_plural = 'Species'

    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="species")
    k = models.IntegerField(help_text='Weight of calculating points')

    def __unicode__(self):
        return self.name

class Fish(models.Model):
    class Meta:
        verbose_name_plural = 'Fish'

    user = models.ForeignKey(User)
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    witness = models.CharField(max_length=50)
    species = models.ForeignKey(Species)
    image = models.ImageField(upload_to="fish")
