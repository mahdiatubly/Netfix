from django import forms
from .models import Service, Company

class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ['requests_count', 'rating', 'company']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ServiceCreateForm, self).__init__(*args, **kwargs)

        # Set initial values based on the signed-in user
        if user and user.is_authenticated:
            company = Company.objects.get(user=user)
            if company.field == 'All in One':
                # If the company is "All in One", allow the user to choose the field
                self.fields['field'] = forms.ChoiceField(
                    choices=Service._meta.get_field('field').choices)
            else:
                # Exclude the company field for other types of companies
                del self.fields['field']