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
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to="fish")

    STATUS = (
        ('normal', 'Normal'),
        ('removed', 'Removed'),
    )
    status = models.CharField(max_length=10, choices=STATUS, default='normal')

    create = models.DateTimeField(auto_now_add=True)

    def save(self, *a, **kw):
        self.points = int(round(self.weight * self.species.k))
        super(Fish, self).save(*a, **kw)


class Comment(models.Model):
    user = models.ForeignKey(User)
    fish = models.ForeignKey(Fish)
    content = models.CharField(max_length=2000)

    create = models.DateTimeField(auto_now_add=True)
