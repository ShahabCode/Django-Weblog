from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post, User, Account


class TicketForm(forms.Form):
    STATUS_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=STATUS_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن وارد شده عددی نیست!")
            else:
                return phone


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError("نام وارد شده کوتاه است!")
            else:
                return name

    class Meta:
        model = Comment
        fields = ('name', 'body')


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label="تصویر اول", required=False)
    image2 = forms.ImageField(label="تصویر دوم", required=False)

    class Meta:
        model = Post
        fields = ('title', 'description', 'reading_time')


class SearchForm(forms.Form):
    query = forms.CharField()


# class LoginForm(forms.Form):
#     username = forms.CharField(required=True)
#     password = forms.CharField(required=True ,widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='password')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label='repeat password')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('پسوردها مطابقت ندارند!')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('date_of_birth', 'bio', 'job', 'photo')