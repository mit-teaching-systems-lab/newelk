from django import forms
from chat.models import Scenario

BOOL_CHOICES = ((True, 'True'), (False, 'False'))

# class ScenarioForm(forms.Form):
#     scenario_name = forms.CharField(max_length=50)
#     student_background = forms.CharField(widget=forms.Textarea)
#     student_profile = forms.CharField(widget=forms.Textarea)
#     teacher_background = forms.CharField(widget=forms.Textarea)
#     teacher_objective = forms.CharField(widget=forms.Textarea)
#     visible_to_players = forms.BooleanField()


class ScenarioForm(forms.ModelForm):
    # scenario_name = forms.CharField(max_length=50)
    # student_background = forms.CharField(widget=forms.Textarea)
    # student_profile = forms.CharField(widget=forms.Textarea)
    # teacher_background = forms.CharField(widget=forms.Textarea)
    # teacher_objective = forms.CharField(widget=forms.Textarea)
    # visible_to_players = forms.BooleanField()
    class Meta:
        model = Scenario
        fields = ['scenario_name','student_background','student_profile','teacher_background','teacher_objective','visible_to_players']