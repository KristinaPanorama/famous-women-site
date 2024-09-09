from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from captcha.fields import CaptchaField

from women.models import Category, Husband, Women


@deconstructible
class RusValidator:
    ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    code = 'ru'

    def __init__(self, message=None):
        self.message = message if message else "Only rus letters"

    def __call__(self, value, *args, **kwargs):
        if not set(value) <= set(self.ALLOWED_CHARS):
            raise ValidationError(self.message, code=self.code, params={'value': value})


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), label='Муж', empty_label='Не замужем', required=False)

    class Meta:
        model = Women
        fields = ['title', 'slug', 'photo', 'content', 'is_published', 'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 70, 'rows': 5})
        }
        labels = {
            'slug': 'URL',
            'photo': 'Фото'
        }

    def clean_title(self):
        max_length = 50
        title = self.cleaned_data['title']
        if len(title) > max_length:
            raise ValidationError('Длина превышает 50 символов')

        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='E-mail', widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
