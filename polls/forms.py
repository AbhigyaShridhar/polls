from django import forms

from .models import User, Choice, Poll

"""
class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Cofirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            return False
        return True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
"""

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['content', 'expiry', 'public']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']
