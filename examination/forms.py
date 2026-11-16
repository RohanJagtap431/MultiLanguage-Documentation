
from django import forms
from django.contrib.auth import get_user_model

from .models import ClassAccess

User = get_user_model()


class ClassAccessForm(forms.ModelForm):

    student = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Student",
        empty_label="Select Student",
    )

    class Meta:
        model = ClassAccess
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["student"].label_from_instance = (
            lambda user: f"{user.name} ({user.mobile_number})"
        )
