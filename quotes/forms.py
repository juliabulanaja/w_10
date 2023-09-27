from django.utils import timezone

from django import forms
from .models import Author, Tag, Quote


class AuthorForm(forms.ModelForm):
    fullname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control",
                                                                                            "id": "fullname"}))
    born_location = forms.CharField(max_length=150, required=True,
                                    widget=forms.TextInput(attrs={"class": "form-control",
                                                                  "id": "born_location"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}))
    born_date = forms.DateField(required=True, initial=timezone.now,
                                widget=forms.DateInput(attrs={'type': 'date', "id": "born_date"}))

    class Meta:
        model = Author
        fields = ['fullname', 'description', 'born_date', 'born_location']


class TagForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control",
                                                                                        "id": "name"}))

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(forms.ModelForm):
    quote = forms.CharField(max_length=300, required=True, widget=forms.TextInput(attrs={"class": "form-control",
                                                                                         "id": "quote"}))
    author = forms.ModelChoiceField(queryset=Author.objects.all())

    class Meta:
        model = Quote
        fields = ["quote", "author"]
        exclude = ["tags"]
