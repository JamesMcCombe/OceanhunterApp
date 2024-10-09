from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Division, GENDER_CHOICES, CITY_CHOICES, Profile


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("This email does not exist.")
        return email


DOB_INPUT_FORMATS = ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d']


class ExtraProfileForm(forms.ModelForm):
    division = forms.ModelChoiceField(queryset=Division.objects.all(), empty_label='Select Region')

    class Meta:
        model = Profile
        fields = ('division', )

    def clean_division(self):
        if self.instance and self.instance.division and self.instance.division != self.cleaned_data['division']:
            raise forms.ValidationError('Once set, division cannot be changed.')
        return self.cleaned_data['division']


class SignupForm(ExtraProfileForm):
    error_css_class = 'error'
    required_css_class = 'required'

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        'email_exists': _("Email address already exists."),
    }

    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")
    email = forms.EmailField(label="Email address")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )
        return email

    def clean_division(self):
        if self.instance.pk and self.instance.profile.division and self.instance.profile.division != self.cleaned_data['division']:
            raise forms.ValidationError('Once set, division cannot be changed.')
        return self.cleaned_data['division']

    def save(self, commit=True):
        user = super().save(commit=False)
        data = self.cleaned_data
        user.username = data['email']  # use email as username
        user.set_password(data['password1'])
        if commit:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            p = user.profile
            p.division = data['division']
            p.save()
        return user
