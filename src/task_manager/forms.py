from django import forms
from django.forms import ModelForm
from account.models import User
from task_manager.models import Tasks, Tags, Attachments
from django.core.exceptions import ValidationError
from django.forms import Textarea

class CommentForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="user",
    )
    task = forms.ModelChoiceField(
        queryset=Tasks.objects.all(),
        label="user task"
    )
    message = forms.CharField(
        label="Comments",
        widget=forms.Textarea(),
    )
    user.widget.attrs.update({'class':'user'})

class TasksForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'priority']
        widgets = {
            "description": Textarea(attrs={"cols": 40, "rows": 5}),
        }

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        priority = cleaned_data.get("priority")

        if not description:
            if priority > 2:
                raise ValidationError(
                    "Приоритет для задач без описания не может быть больше 2"
                )

class TagsForm(ModelForm):
    class Meta:
        model = Tags
        fields = ['name', 'tasks']

class AttachmentsForm(ModelForm):
    class Meta:
        model = Attachments
        fields = ["name","photo","task"]