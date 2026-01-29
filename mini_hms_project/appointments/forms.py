from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('patient', 'Patient')])
    class Meta(UserCreationForm.Meta): model = User; fields = UserCreationForm.Meta.fields + ('email',)