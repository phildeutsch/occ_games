from django import forms

from .models import TfPlayer


class TfNewPlayerForm(forms.ModelForm):
    class Meta:
        model = TfPlayer
        fields = ('first_name', 'last_name',)
