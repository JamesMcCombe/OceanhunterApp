from django.db import models
from django.db.models import F
from django.contrib.auth.models import User


class Species(models.Model):
    class Meta:
        verbose_name_plural = 'Species'

    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="species", null=True)
    base = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True, default=0,
                               help_text='Base of calculating points')

    def __str__(self):
        return self.name

    def recalculate_all(self):
        self.fish_set.update(points=F('weight') * 100. / self.base)


class Division(models.Model):
    name = models.CharField(max_length=255)
    species = models.ManyToManyField(Species, related_name='division')

    def __str__(self):
        return self.name


class FishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status='removed')


class Fish(models.Model):
    class Meta:
        verbose_name_plural = 'Fish'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    witness = models.CharField(max_length=50)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    points = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    image = models.ImageField(upload_to="fish")

    STATUS = (
        ('normal', 'Normal'),
        ('removed', 'Removed'),
    )
    status = models.CharField(max_length=10, choices=STATUS, default='normal')

    create = models.DateTimeField(auto_now_add=True)

    objects = FishManager()

    def save(self, *args, **kwargs):
        self.calculate_points()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.status = 'removed'
        self.save()

    def calculate_points(self):
        self.points = 100 + int(self.weight * 100)  # 100 points per species + 1 point per 10 grams

    def __str__(self):
        return str(self.pk)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
