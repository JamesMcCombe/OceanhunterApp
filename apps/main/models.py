from django.db import models

class Species(models.Model):
    class Meta:
        verbose_name_plural = 'Species'

    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="species")
    k = models.IntegerField(help_text='Weight of calculating points')
