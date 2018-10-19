from django import forms

BOOL_CHOICES = ((True, 'True'), (False, 'False'))

class ScenarioForm(forms.ModelForm):
    scenario_name = forms.CharField(max_length=50)
    student_background = forms.CharField(widget=forms.Textarea)
    student_profile = forms.CharField(widget=forms.Textarea)
    teacher_background = forms.CharField(widget=forms.Textarea)
    teacher_objective = forms.CharField(widget=forms.Textarea)
    visible_to_players = forms.BooleanField()