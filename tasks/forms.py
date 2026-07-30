from django import forms

from .models import TaskSubmission


class TaskSubmissionForm(forms.ModelForm):

    class Meta:
        model = TaskSubmission
        fields = ["file", "comment"]