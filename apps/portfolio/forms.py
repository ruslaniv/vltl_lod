from django import forms


class TickerForm(forms.Form):
    ticker = forms.SelectMultiple()
