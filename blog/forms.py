from django import forms
from .models import Comment, Post


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
    image1 = forms.ImageField(label="تصویر اول")
    image2 = forms.ImageField(label="تصویر دوم")

    class Meta:
        model = Post
        fields = ('title', 'description', 'reading_time')


class SearchForm(forms.Form):
    query = forms.CharField()


# class LoginForm(forms.Form):
#     username = forms.CharField(required=True)
#     password = forms.CharField(required=True ,widget=forms.PasswordInput)