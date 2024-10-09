from django import forms
from django.contrib.auth.models import User
from django.utils.encoding import force_str  # force_text is deprecated, use force_str
from . import models as m
from apps.accounts import models as am
from apps.main.models import Division


class TeamForm(forms.ModelForm):
    class Meta:
        model = am.Team
        fields = ('name',)


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

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields['species'].queryset = self.request.user.profile.get_species()


class CommentForm(forms.ModelForm):
    class Meta:
        model = m.Comment
        fields = ('fish', 'content')


class FilterForm(forms.Form):
    UNIT_CHOICES = (('solo', 'Solo'), ('team', 'Team'))
    AGE_CHOICES = (('junior', 'Junior'), ('open', 'Open Age'))

    TYPE_CHOICES = [
        ('total', 'Biggest six'),
        ('biggest', 'Biggest crayfish')
    ]

    division = forms.ModelChoiceField(queryset=Division.objects.all(), required=False)
    type = forms.ChoiceField(widget=forms.RadioSelect, choices=TYPE_CHOICES, initial='total')

    def filters(self):
        """For leaderboard. Get non-empty fields and get the label of the choice."""
        filters = []
        for field in self:
            choice_value = field.value()
            choices = field.field.choices
            if choice_value:
                choice_label = get_choice_label(choices, choice_value)
                field.choice_label = choice_label
                filters.append(field)
        return filters

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        data = kwargs.get('data') or (args[0] if args else {})
        if not data.get('division') and self.request and self.request.user.is_authenticated:
            data['division'] = str(self.request.user.profile.division.pk)

        super().__init__(data, *args, **kwargs)


def get_choice_label(choices, value):
    """ Get label from Django form choices."""
    for choice_value, choice_label in choices:
        if choice_value is None:
            choice_value = ''
        choice_value = force_str(choice_value)
        if isinstance(choice_label, (list, tuple)):
            sub_choices = choice_label
            choice_label = get_choice_label(sub_choices, value)
            if choice_label:
                return choice_label
        else:
            if value == choice_value:
                return choice_label


if __name__ == '__main__':
    import doctest
    doctest.testmod()
