from django import forms
from .models import Chat, BlogPost, TravelPlanTrip
from django.contrib.auth.models import User
from user.models import Profile, Vibes


class ChatForm(forms.ModelForm):
    # receiver = forms.ModelChoiceField(queryset=User.objects.all())
    # sender = forms.ModelChoiceField(queryset=User.objects.all())
    class Meta:
        model = Chat
        fields = ['message']


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(
        required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}), required=False)
    personal_favorite_trip_blog = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    vibes = forms.ModelMultipleChoiceField(
        queryset=Vibes.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control vibes-multiple'}),
        required=False
    )
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'email',
            'number',
            'profile_pic',
            'bio',
            'personal_favorite_trip_blog',
            'vibes'
        ]
    def save(self, commit=True):
            instance = super(ProfileForm, self).save(commit=False)

            # Save the profile instance first
            if commit:
                instance.save()

            # Handle the vibes field
            if 'vibes' in self.cleaned_data:
                instance.vibes.set(self.cleaned_data['vibes'])

            return instance

class TravelPlanForm(forms.ModelForm):
    class Meta:
        model = TravelPlanTrip
        fields = '__all__'
        exclude = ['group_name']

    def save(self, commit=True):
        form_data = self.cleaned_data
        if form_data['share_facilities'] == 'no':
            form_data['share_every_facility'] = None
            form_data['facilities'] = None
            form_data['facilities_image'] = None
        elif form_data['share_facilities'] == 'yes':
            print(form_data)
            form_data['share_facilities'] = True
            
        return super().save(commit=commit)
