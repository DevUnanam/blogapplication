from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.decorators.http import require_http_methods
from blog.forms import CustomUserCreationForm, UserProfileForm, CustomAuthenticationForm


class RegisterView(CreateView):
    """
    User registration view
    """
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('blog:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Welcome {username}! Your account has been created successfully.')
        
        # Log the user in after registration
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        if user:
            login(self.request, user)
        
        return response


def login_view(request):
    """
    User login view
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('blog:home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """
    Custom logout view that handles both GET and POST requests
    """
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f'You have been logged out successfully. See you later, {username}!')
    
    return redirect('blog:home')


@login_required
def edit_profile(request):
    """
    Edit user profile view
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('blog:user_profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user.profile, user=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})