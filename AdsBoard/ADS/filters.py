from django_filters import FilterSet, ModelChoiceFilter
from .models import Response, User, Ad
from django.utils.translation import gettext as _


class AdFilter(FilterSet):

    class Meta:
        model = Response
        fields = {'ad'}

    def __init__(self, *args, **kwargs):
        super(AdFilter, self).__init__(*args, **kwargs)
        self.filters['ad'].queryset = Ad.objects.filter(author_id=kwargs['request'])