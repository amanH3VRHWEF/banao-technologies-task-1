from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Slot

class SignUpForm(UserCreationForm):
    # Requirement: Role-based selection for Doctor or Patient
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, help_text="Select your account type")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role',)

class SlotForm(forms.ModelForm):
    # Requirement: Doctor-specific form to add available slots
    class Meta:
        model = Slot
        fields = ['start_time']
        widgets = {
            # This 'datetime-local' widget provides a calendar/time picker in the browser
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        # You can add logic here to prevent picking past dates if needed
        return start_time