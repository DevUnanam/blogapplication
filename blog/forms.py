from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Comment, UserProfile, Genre


class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'excerpt', 'genre', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'placeholder': 'Enter your post title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'rows': 15,
                'placeholder': 'Write your story...'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'rows': 3,
                'placeholder': 'Brief description of your post...'
            }),
            'genre': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white'
            }),
            'featured_image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white'
            }),
        }


class CommentForm(forms.ModelForm):
    """
    Form for creating comments and replies
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'rows': 3,
                'placeholder': 'Write your comment...'
            }),
        }


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile
    """
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'website', 'location', 'dark_mode']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'placeholder': 'https://yourwebsite.com'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'placeholder': 'Your location'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white'
            }),
            'dark_mode': forms.CheckboxInput(attrs={
                'class': 'w-6 h-6 text-yellow-400 bg-gray-100 border-gray-300 rounded focus:ring-yellow-400 dark:focus:ring-yellow-400 dark:bg-gray-600 dark:border-gray-500'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Update user fields
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name'] 
            user.email = self.cleaned_data['email']
            user.save()
        return profile


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form with additional fields
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'placeholder': 'Choose a username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'placeholder': 'Your email address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
                'placeholder': 'Last name'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
            'placeholder': 'Confirm your password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom login form with styled fields
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400 dark:bg-gray-700 dark:text-white',
            'placeholder': 'Enter your password'
        })