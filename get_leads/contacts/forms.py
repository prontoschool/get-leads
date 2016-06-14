from django import forms


class ContactForm(forms.Form):
    firstname = forms.CharField(
        widget=forms.TextInput(),
        required=True
    )

    lastname = forms.CharField(
        widget=forms.TextInput(),
        required=True
    )

    email = forms.EmailField(
        required=True
    )
