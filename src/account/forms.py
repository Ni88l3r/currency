from account.models import User
from account.tasks import send_signup_email_async

from django import forms


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'User with given email exists!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError(f'Passwords do not match!')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.username = instance.email
        instance.is_active = False
        instance.set_password(self.cleaned_data['password1'])
        instance.save()

        # send_signup_email_async.delay(instance)
        send_signup_email_async(instance.id)
        return instance


class ChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = 'old_password', 'new_password1', 'new_password2'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Wrong password!')
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['new_password1'] != cleaned_data['new_password2']:
                raise forms.ValidationError('Password mismatch!')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data['new_password1'])
        instance.save()
        return instance
