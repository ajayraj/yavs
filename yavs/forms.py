from django import forms

class SignInForm(forms.Form):
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", max_length=48, widget=forms.PasswordInput())

class SignUpForm(forms.Form):
    email = forms.CharField(label="Email", max_length=20)
    username = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", max_length=48, widget=forms.PasswordInput())

class UploadVideoForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50)
    description = forms.CharField(label="Description", max_length=500)
    file = forms.FileField(label="Video")

class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", max_length=500)
    video = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
