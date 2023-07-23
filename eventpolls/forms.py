from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Event


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# Create the form class.
class EventForm(forms.ModelForm):
    name = forms.CharField(required=True, max_length=50)
    description = forms.CharField(required=False, max_length=100)

    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
        ]