from django import forms


class CompanyForm(forms.Form):
    company_name = forms.CharField(max_length=10, required=False)
    parking_name = forms.CharField(max_length=10, required=False)


class CompanyGetForm(forms.Form):
    company_name = forms.CharField(max_length=10,required=False)
    parking_name = forms.CharField(max_length=10, required=False)