from django import forms
from .models import Service, Company

class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['requests_count', 'rating', 'company']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ServiceCreateForm, self).__init__(*args, **kwargs)

        if user and user.is_authenticated:
            company = Company.objects.get(user=user)
            if company.field == 'All in One':
                self.fields['field'] = forms.ChoiceField(
                    choices=Service._meta.get_field('field').choices, widget=forms.Select(attrs={'class': 'form-control'}))
            else:
                del self.fields['field']