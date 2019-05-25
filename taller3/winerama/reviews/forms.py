from django.forms import ModelForm, Textarea
from reviews.models import Review
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    #print( "COMO MANDE")
    city = forms.CharField(required=True)

    class Meta:
    	model = User
    	fields = (
    		'username',
    		'first_name',
    		'last_name',
    		'email',
    		'city',
    		'password1',
    		'password2'
    	)

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.city = self.cleaned_data['city']

        if commit:
        	user.save()
        return user


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 40, 'rows': 15}),
        }

