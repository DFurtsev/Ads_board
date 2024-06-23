from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Ad, Response
from django.core.exceptions import ValidationError


class AdForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)
        self.fields['head'].label = "Укажите название"
        self.fields['text'].label = "Введите описание"
        self.fields['category'].label = "Выберите категорию"


    class Meta:
        model = Ad
        fields = [
            'head',
            'text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 5:
            raise ValidationError({"text": "Содержание должно быть больше 5 слов."})
        heading = cleaned_data.get("heading")
        if heading == text:
            raise ValidationError("Содержание должно отличаться от заголовка.")
        return cleaned_data


class ResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Введите текст"

    class Meta:
        model = Response
        fields = [
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        return cleaned_data
