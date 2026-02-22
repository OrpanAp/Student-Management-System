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
    class Meta:
        model = models.StudentResult
        fields = (
            'roll',
            'year',
            'semester',
            'subject',
            'cgpa'
        )

    def clean(self):
        cleaned_data = super().clean()
        roll = cleaned_data.get('roll')
        user = roll.user if roll else None
        year = cleaned_data.get('year')
        semester = cleaned_data.get('semester')
        subject = cleaned_data.get('subject')

        if models.StudentResult.objects.filter(
            user=user,
            year=year,
            semester=semester,
            subject=subject
        ).exists():
            raise forms.ValidationError(
                "This subject already exists for this student in this semester and year."
            )

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 Only show students
        self.fields['roll'].queryset = models.StudentProfile.objects.select_related('user').filter(user__role='Student')
        
class StudentAddAttandance(forms.ModelForm):
    class Meta:
        model = models.StudentAttendance
        fields = (
            'roll',
            'subject',
            'status',
        )
        
class StudentResultUpdate(forms.ModelForm):
    class Meta:
        model = models.StudentResult
        fields = (
            'year',
            'semester',
            'subject',
            'cgpa',
        )
        
class SubjectAssign(forms.ModelForm):
    class Meta:
        model = models.Subject
        fields = '__all__'