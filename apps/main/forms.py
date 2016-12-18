from django import forms
from django.contrib.auth.models import User
from django.utils.encoding import force_text
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
        super(FishForm, self).__init__(*args, **kwargs)

        self.fields['species'].queryset = self.request.user.profile.get_species()


class CommentForm(forms.ModelForm):
    class Meta:
        model = m.Comment
        fields = ('fish', 'content')


class FilterForm(forms.Form):
    UNIT_CHOICES = (('solo', 'Solo'), ('team', 'Team'))
    AGE_CHOICES = (('junior', 'Junior'), ('open', 'Open Age'))

    # city = forms.ChoiceField(label="City", choices=am.CITY_CHOICES, required=False)
    species = forms.ModelChoiceField(queryset=m.Species.objects, label="Fish Species", required=False)
    # area = forms.ChoiceField(widget=forms.RadioSelect, choices=am.AREA_CHOICES, required=False)
    division = forms.ModelChoiceField(queryset=Division.objects, required=False)
    unit = forms.ChoiceField(widget=forms.RadioSelect, choices=UNIT_CHOICES, initial='solo')
    team_kind = forms.ChoiceField(widget=forms.RadioSelect, choices=am.TEAM_KINDS, required=False)
    age = forms.ChoiceField(widget=forms.RadioSelect, choices=AGE_CHOICES, required=False)
    # gender = forms.ChoiceField(widget=forms.RadioSelect, choices=am.GENDER_CHOICES, required=False)

    def filters(self):
        """For leader board. Get non empty field and get the label of the choice
        """
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
        self.request = kwargs.pop('request')
        # TODO: uncomment this to enable setting division by default
        # data = kwargs.get('data') or args[0]
        # if not data.get('division') and self.request.user.is_authenticated():
        #     data['division'] = str(self.request.user.profile.division.pk)

        super(FilterForm, self).__init__(*args, **kwargs)


def get_choice_label(choices, value):
    """ Get label from django form choices
    >>> get_choice_label((('1', 'Northland'), ('2', 'Auckland')), '1')
    'Auckland'
    >>> get_choice_label(((1, 'Northland'), (2, 'Auckland')), '1')
    'Auckland'
    >>> get_choice_label([('', 'Region'), ('North Island', ((1, 'Northland'), (2, 'Auckland'))), ('South Island', (('3', 'XXX')))], '1')
    'Auckland'
    """
    for choice_value, choice_label in choices:
        if choice_value is None:
            choice_value = ''
        choice_value = force_text(choice_value)
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
