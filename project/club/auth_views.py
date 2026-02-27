"""
Authentication views for user registration, login, and logout.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .auth_forms import UserRegistrationForm, UserLoginForm
from .emails import send_welcome_email_to_user


def register_view(request):
    """
    Handle user registration.
    Creates a new user account and sends a welcome email.
    """
    if request.user.is_authenticated:
        # User is already logged in
        messages.info(request, 'You are already logged in.')
        return redirect('club:main')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()
            
            # Send welcome email
            email_sent = send_welcome_email_to_user(user)
            
            # Log the user in automatically
            login(request, user)
            
            # Success message
            if email_sent:
                messages.success(
                    request,
                    f'Welcome {user.username}! Your account has been created successfully. '
                    f'A welcome email has been sent to {user.email}.'
                )
            else:
                messages.success(
                    request,
                    f'Welcome {user.username}! Your account has been created successfully.'
                )
            
            return redirect('club:main')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """
    Handle user login.
    """
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('club:main')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect to next page if specified, otherwise to main
                next_page = request.GET.get('next', 'club:main')
                return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Handle user logout.
    """
    if request.method == 'POST':
        username = request.user.username
        logout(request)
        messages.success(request, f'Goodbye, {username}! You have been logged out.')
        return redirect('club:main')
    
    return render(request, 'auth/logout_confirm.html')


@login_required
def profile_view(request):
    """
    Display user profile.
    """
    return render(request, 'auth/profile.html', {'user': request.user})
