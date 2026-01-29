from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Slot, Booking
from .forms import SignUpForm
import requests
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['role'] == 'doctor': user.is_doctor = True
            else: user.is_patient = True
            user.save(); login(request, user)
            requests.post("http://localhost:3000/dev/send-email", json={"type": "SIGNUP_WELCOME", "email": user.email})
            return redirect('dashboard')
    return render(request, 'signup.html', {'form': SignUpForm()})
def dashboard(request):
    if request.user.is_doctor: return render(request, 'doctor_dashboard.html', {'slots': Slot.objects.filter(doctor=request.user)})
    return render(request, 'patient_dashboard.html', {'slots': Slot.objects.filter(is_booked=False)})