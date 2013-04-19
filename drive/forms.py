from django import forms
from .models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ('user', 'added',)
        
class SearchForm(forms.Form):
    query = forms.CharField(max_length=64, required=False, widget=forms.TextInput(attrs={'class': 'search-query',
                                                                                         'placeholder': 'Search Files',
                                                                                         'id': 'search-input'}))