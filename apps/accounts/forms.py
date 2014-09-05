from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from . import models as m


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            m.User.objects.get(email=email)
        except Exception, e:
            raise forms.ValidationError(str(e))
        return email


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

    # other fields
    # address = forms.CharField(label="Address")
    #suburb = forms.CharField(label="Surburb")
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=m.GENDER_CHOICES)
    area = forms.ChoiceField(widget=forms.RadioSelect, choices=m.AREA_CHOICES)
    city = forms.CharField(label="City")
    dob = forms.DateField(label="Date of Birth")
    #postcode = forms.CharField(label="Postcode")
    #phone = forms.CharField(label="Phone Number")

    email = forms.EmailField(label="Email address")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email):
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )
        return email

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError(
    #             self.error_messages['password_mismatch'],
    #             code='password_mismatch',
    #         )
    #     return password2

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
            # other fields here
            #p.address = data['address']
            #p.suburb = data['suburb']
            #p.city = data['city']
            #p.postcode = data['postcode']
            #p.phone = data['phone']
            p.gender = data['gender']
            p.area = data['area']
            p.city = data['city']
            p.dob = data['dob']
            p.save()
        return user
