from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.accounts.models import Division, Profile
from apps.accounts.models import Invite


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except Exception, e:
            raise forms.ValidationError(str(e))
        return email


DOB_INPUT_FORMATS = ['%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d']


class ExtraProfileForm(forms.ModelForm):
    division = forms.ModelChoiceField(queryset=Division.objects, empty_label='Choose group')
    dob = forms.DateField(label="Date of Birth", input_formats=DOB_INPUT_FORMATS)

    class Meta:
        model = Profile
        fields = ('division', 'dob')

    def clean_division(self):
        if self.instance and self.instance.division and self.instance.division != self.cleaned_data['division']:
            raise forms.ValidationError('Once set, division can not be changed.')
        else:
            return self.cleaned_data['division']


class SignupForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
        'email_exists': _("Email address already exists."),
    }

    first_name = forms.CharField(label="First name")
    last_name = forms.CharField(label="Last name")

    division = forms.ModelChoiceField(queryset=Division.objects, empty_label='Choose group')
    dob = forms.DateField(label="Date of Birth", input_formats=DOB_INPUT_FORMATS)

    email = forms.EmailField(label="Email address")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def get_invite(self):
        invitation_code = self.request.GET.get('invitation')
        invite = None
        if invitation_code:
            invite = Invite.objects.filter(key=invitation_code).first()

        return invite

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')

        invite = self.get_invite()

        if invite and 'data' in kwargs:
            kwargs['data'] = kwargs['data'].copy()
            kwargs['data']['division'] = invite.inviter.profile.division.pk

        super(SignupForm, self).__init__(*args, **kwargs)

        if invite:
            self.fields['email'].initial = invite.ref
            self.fields['email'].widget.attrs['readonly'] = True
            self.fields['division'].initial = invite.inviter.profile.division
            self.fields['division'].widget.attrs['disabled'] = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email):
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )
        return email

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        data = self.cleaned_data
        user.username = data['email']  # use email as username also
        user.set_password(data['password1'])
        if commit:
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.save()
            p = user.profile

            p.division = data['division']
            p.dob = data['dob']
            p.save()
        return user


