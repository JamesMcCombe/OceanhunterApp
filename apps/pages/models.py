from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Page(models.Model):
    STATUS_CHOICES = (
        ('draft', 'draft'),
        ('published', 'published'),
    )
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    template = models.CharField(max_length=50, default='pages/page.html')

    user = models.ForeignKey(User, editable=False)
    order = models.IntegerField(default=1000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    touch  = models.DateTimeField(default=datetime.now, editable=False)
    publish  = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ('order', '-publish')

    def __unicode__(self):
        return self.title

