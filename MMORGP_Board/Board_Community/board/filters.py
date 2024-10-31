from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    date = DateFilter(
        field_name='datetime_in',
        label='Date',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
            'heading': ['icontains'],
            'author': ['exact'],
        }
