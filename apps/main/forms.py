from django import forms
from django.contrib.auth.models import User
from . import models as m


class FishForm(forms.ModelForm):
    class Meta:
        model = m.Fish
        fields = ('species', 'weight', 'witness', 'image')
        labels = {
            'species': 'Fish type',
        }
        help_texts = {
            'weight': 'Kgs',
            'witness': 'Enter name',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = m.Comment
        fields = ('fish', 'content')
