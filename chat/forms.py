from django import forms

BOOL_CHOICES = ((True, 'True'), (False, 'False'))

class ScenarioForm(forms.Form):
    scenario_name = forms.CharField(max_length=50)
    student_background = forms.TextField()
    student_profile = forms.TextField()
    teacher_background = forms.TextField()
    teacher_objective = forms.TextField()
    visible_to_players = forms.BooleanField(
        choices=BOOL_CHOICES,
        default=True,
    )