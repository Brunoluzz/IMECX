from django import forms

from .models import TaskSubmission


class TaskSubmissionForm(forms.ModelForm):

    def __init__(self, *args, disabled=False, **kwargs):
        super().__init__(*args, **kwargs)

        if disabled:
            for field in self.fields.values():
                field.disabled = True

    class Meta:
        model = TaskSubmission
        fields = ["file", "comment"]