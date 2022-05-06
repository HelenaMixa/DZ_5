from django import forms
from Dance_Info.models import *


class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = (
            'coach_surname',
            'coach_name',
            'telephone',
            'mail',
        )


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = (
            'club_name',
            'coach',
            'city',
        )


class DancerForm(forms.ModelForm):
    class Meta:
        model = Dancer
        fields = '__all__'
