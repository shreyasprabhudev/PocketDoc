from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, DoctorForm, PatientForm
from .models import UserInformation, Doctor, Patient

def home(request):
    if request.user.is_authenticated:
        return redirect('patient_dashboard')
    else:
        return render(request, 'home.html')

    
def patient_dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to access the dashboard.")
        return redirect('login')
    return render(request, 'patient_dashboard.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('patient_dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('patient_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            is_doctor = request.POST.get('is_doctor', 'off') == 'on'
            user_info = UserInformation.objects.create(
                user=new_user,
                first_name=user_form.cleaned_data['first_name'],
                last_name=user_form.cleaned_data['last_name'],
                email=user_form.cleaned_data['email'],
                phone=user_form.cleaned_data['phone_number'],
                address=user_form.cleaned_data['address'],
                city=user_form.cleaned_data['city'],
                state=user_form.cleaned_data['state'],
                zipcode=user_form.cleaned_data['zipcode'],
                is_doctor=is_doctor
            )
            login(request, new_user)
            return redirect('patient_dashboard')
        else:
            messages.error(request, user_form.errors)
    else:
        user_form = SignUpForm()
    return render(request, 'register.html', {'form': user_form})


def user_profile(request, user_id):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserInformation, user_id=user_id)
        if hasattr(request.user, 'doctor'):
            form = DoctorForm(instance=request.user.doctor)
        elif hasattr(request.user, 'patient'):
            form = PatientForm(instance=request.user.patient)
        else:
            return redirect('home')

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Profile Updated Successfully!")
                return redirect('profile', user_id=user_id)

        return render(request, 'profile.html', {'form': form, 'profile': user_profile})
    else:
        messages.error(request, "You Must Be Logged In To View This Page...")
        return redirect('home')

