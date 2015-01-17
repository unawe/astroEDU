from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(label='Query', required=True)
    age = forms.CharField(label='age', required=False)
    level = forms.CharField(label='level', required=False)
    time = forms.CharField(label='time', required=False)
    group = forms.CharField(label='group', required=False)
    supervised = forms.CharField(label='supervised', required=False)
    cost = forms.CharField(label='cost', required=False)
    location = forms.CharField(label='location', required=False)
    skills = forms.CharField(label='skills', required=False)
    learning = forms.CharField(label='learning', required=False)
