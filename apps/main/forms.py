from django import forms
from django.contrib.auth.models import User
from . import models as m
from accounts import models as am


class TeamForm(forms.ModelForm):
    class Meta:
        model = am.Team
        fields = ('name', 'kind')


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


class FilterForm(forms.Form):
    UNIT_CHOICES = (('solo', 'Solo'), ('team', 'Team'))
    TEAM_CHOICES = (('family', 'Family Team'), ('open', 'Open Team'))
    AGE_CHOICES = (('junior', 'Junior'), ('open', 'Open Age'))

    city = forms.ChoiceField(label="City", choices=am.CITY_CHOICES)
    species = forms.ModelChoiceField(queryset=m.Species.objects, label="Fish Species")
    area = forms.ChoiceField(widget=forms.RadioSelect, choices=am.AREA_CHOICES)
    unit = forms.ChoiceField(widget=forms.RadioSelect, choices=UNIT_CHOICES, initial='solo')
    team = forms.ChoiceField(widget=forms.RadioSelect, choices=TEAM_CHOICES)
    age = forms.ChoiceField(widget=forms.RadioSelect, choices=AGE_CHOICES)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=am.GENDER_CHOICES)
