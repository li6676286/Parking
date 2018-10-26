from django import forms


class ParkingPostForm(forms.Form):
    company_id = forms.CharField(required=False)
    parking_name = forms.CharField(required=False)