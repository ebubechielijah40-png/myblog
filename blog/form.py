from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'slug')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter post content', 'rows': 8}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post slug'}),
        }
        labels = {'slug': 'Post Slug'}
        help_texts = {'slug': 'A unique identifier for the post, used in the URL.'}

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title

    def clean(self):
        cleaned = super().clean()
        title = cleaned.get('title')
        slug = cleaned.get('slug')
        if title and slug and slug in title:
            raise forms.ValidationError('Slug should not be part of the title.')
        return cleaned
        
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user