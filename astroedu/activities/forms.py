from haystack.forms import FacetedSearchForm
from django import forms
from astroedu.activities.models import Activity


class MultiFacetedSearchForm(FacetedSearchForm):
    # age = forms.ChoiceField(choices=Activity.AGE_CHOICES, required=False)
    # age = forms.MultipleChoiceField(choices=Activity.AGE_CHOICES, required=False, widget=forms.CheckboxSelectMultiple, )
    # level = forms.MultipleChoiceField(choices=Activity.LEVEL_CHOICES, required=False, widget=forms.CheckboxSelectMultiple, )
    # level = forms.MultipleChoiceField(choices=('1', '2'), required=False, widget=forms.CheckboxSelectMultiple, )
    group = forms.MultipleChoiceField(choices=('1', '2'), required=False, widget=forms.CheckboxSelectMultiple, )
    
    def search(self):
        sqs = super(MultiFacetedSearchForm, self).search()
    
        if not self.is_valid():
            return self.no_query_found()
        # if self.cleaned_data['age']:
        #     sqs = sqs.filter(age=self.cleaned_data['age'])
        # if self.cleaned_data['age']:
        #     opts = ' OR '.join(self.cleaned_data['age'])
        #     sqs = sqs.narrow('age_exact:(%s)' % opts)
        # if self.cleaned_data['level']:
        #     opts = ' OR '.join(self.cleaned_data['level'])
        #     sqs = sqs.narrow('level_exact:(%s)' % opts)
        if self.cleaned_data['group']:
            opts = ' OR '.join(self.cleaned_data['group'])
            sqs = sqs.narrow('group_exact:(%s)' % opts)    
        return sqs
