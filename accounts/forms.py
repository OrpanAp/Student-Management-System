from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class UserCreateForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = (
            'first_name',
            'last_name',
            'email',
            'role',
            'password1',
            'password2',
        )

class StudentCreateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
        
class StudentClassAssignForm(forms.ModelForm):
    class Meta:
        model = models.StudentProfile
        fields = (
            'class_list',
        )
        

class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'role',
        )
        
class StudentUpdateClassAssignForm(forms.ModelForm):
    class Meta:
        model = models.StudentProfile
        fields = (
            'class_list',
            'roll',
        )
        
class StudentAddResult(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=models.User.objects.filter(role="Student"), label="Student"
    )
    
    class Meta:
        model = models.StudentResult
        fields = (
            'user',
            'subject',
            'semester',
            'year',
            'cgpa',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get users who already have results
        existing_users = models.StudentResult.objects.values_list('user', flat=True)

        # Exclude them from queryset
        self.fields['user'].queryset = models.User.objects.filter(
            role="Student"
        ).exclude(id__in=existing_users)
        
class StudentAddAttandance(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=models.User.objects.filter(role="Student"), label="Student"
    )
    
    class Meta:
        model = models.StudentAttendance
        fields = (
            'user',
            'total_class_count',
            'total_attendance_count',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get users who already have results
        existing_users = models.StudentResult.objects.values_list('user', flat=True)

        # Exclude them from queryset
        self.fields['user'].queryset = models.User.objects.filter(
            role="Student"
        ).exclude(id__in=existing_users)