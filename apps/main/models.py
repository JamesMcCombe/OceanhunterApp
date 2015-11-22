from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User


class Species(models.Model):
    class Meta:
        verbose_name_plural = 'Species'

    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="species", null=True)
    # the size of the biggest catch of this species
    base = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True, default=0,
                               help_text='Base of calculating points')

    def __unicode__(self):
        return self.name

    def recalculate_all(self):
        from django.db.models import F
        self.fish_set.update(points=F('weight') * 100. / self.base)


class Division(models.Model):
    name = models.CharField(max_length=255)
    species = models.ManyToManyField(Species, related_name='division')

    def __unicode__(self):
        return u', '.join(map(unicode, self.species.all()))


class FishManager(models.Manager):
    def get_queryset(self):
        return super(FishManager, self).get_queryset().exclude(status='removed')


class Fish(models.Model):
    class Meta:
        verbose_name_plural = 'Fish'

    user = models.ForeignKey(User)
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    witness = models.CharField(max_length=50)
    species = models.ForeignKey(Species)
    points = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    image = models.ImageField(upload_to="fish")

    STATUS = (
        ('normal', 'Normal'),
        ('removed', 'Removed'),
    )
    status = models.CharField(max_length=10, choices=STATUS, default='normal')

    create = models.DateTimeField(auto_now_add=True)

    objects = FishManager()

    def save(self, *a, **kw):
        if not self.pk:
            if self.weight > self.species.base:
                self.species.base = self.weight
                self.species.save()
                self.species.recalculate_all()

        if not self.status == 'removed':
            self.recalculate_points()

        super(Fish, self).save(*a, **kw)

    def delete(self, using=None):
        points = self.points

        self.status = 'removed'
        self.points = 0
        self.save()

        if points == 100:
            self.species.base = Fish.objects.filter(species=self.species).aggregate(max_weight=Max('weight'))['max_weight']
            self.species.save()
            self.species.recalculate_all()

    def recalculate_points(self):
        self.points = (self.weight / self.species.base) * 100

    def __unicode__(self):
        return "%s" % self.pk


class Comment(models.Model):
    user = models.ForeignKey(User)
    fish = models.ForeignKey(Fish)
    content = models.CharField(max_length=2000)

    create = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content




# Divisions
# Snapper, Terakihi, Giant Boarfish, Pink Maomao, Trevally, John Dory
#
# Snapper, Butterfish, Blue Moki, Kahawai, Trevally, John Dory
#
# Blue Cod, Terakihi, Butter Fish, Blue Moki, Kahawai, Trevally
