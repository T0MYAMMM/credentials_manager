from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from apps.backend.models import ActivityLog

def get_client_ip(request):
    """Get the client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_activity(user, action, description, request):
    """Log user activity for security purposes"""
    ActivityLog.objects.create(
        user=user,
        action=action,
        description=description,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )

def login_view(request):
    if request.user.is_authenticated:
        return redirect('frontend:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Log the login activity
            log_activity(user, 'login', f'User logged in from {get_client_ip(request)}', request)
            
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('frontend:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('frontend:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Log the registration activity
            log_activity(user, 'login', f'New user registered and logged in from {get_client_ip(request)}', request)
            
            messages.success(request, f'Welcome to Credentials Manager, {user.first_name}! Your account has been created successfully.')
            return redirect('frontend:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    # Log the logout activity
    log_activity(request.user, 'logout', f'User logged out from {get_client_ip(request)}', request)
    
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('authentication:login')

@login_required
def profile_view(request):
    """User profile view"""
    recent_activities = ActivityLog.objects.filter(user=request.user)[:10]
    
    context = {
        'recent_activities': recent_activities,
    }
    return render(request, 'accounts/profile.html', context)
