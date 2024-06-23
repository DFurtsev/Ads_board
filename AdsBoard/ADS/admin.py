from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from .models import *

from django import forms


class CategoryInline(admin.TabularInline):
    model = AdCategory
    extra = 1


class DistributionAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Distribution
        fields = '__all__'


class DistributionAdmin(admin.ModelAdmin):
    form = DistributionAdminForm


class AdAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Ad
        fields = '__all__'


class AdAdmin(admin.ModelAdmin):
    form = AdAdminForm


admin.site.register(User)
admin.site.register(Category)
admin.site.register(AdCategory)
admin.site.register(Ad, AdAdmin)
admin.site.register(Response)
admin.site.register(Distribution, DistributionAdmin)
