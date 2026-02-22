from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Sum


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False)

    ROLE_CHOICES = {
        ("Student", "Student"),
        ("Teacher", "Teacher"),
        ("Admin", "Admin"),
        ("Manager", "Manager"),
        ("Accounts", "Accounts"),
    }
    role = models.CharField(choices=ROLE_CHOICES, max_length=20, default='student')
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = "Admin"
            self.is_staff = True
        super().save(*args, **kwargs)
    

    @property
    def total_classes_count(self):
        # Use the related_name 'totalclasses' from TotalClassCount
        return self.totalclasses.aggregate(total=Sum('total_class_count'))['total'] or 0
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Subject(models.Model):
    subject = models.CharField(unique=True, max_length=50)
    
    def __str__(self):
        return self.subject

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    CLASS_CHOICES = [(str(i), str(i)) for i in range(0, 11)]
    class_list = models.CharField(choices=CLASS_CHOICES, max_length=10, default='1')
    
    roll = models.CharField(max_length=10)
    
    
    def __str__(self):
        return self.roll
    

class StudentResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)
    semester = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    cgpa = models.FloatField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'year', 'semester', 'subject'],
                name='unique_student_semester_subject'
            )
        ]
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
     
class StudentAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(
        max_length=10,
        choices=(
            ("Present", "Present"),
            ("Absent", "Absent"),
            ("Late", "Late"),
        ), 
        default='Absent'
    )
    created_at = models.DateField(default=timezone.localdate)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['roll', 'subject', 'created_at'],
                name='unique_attendance_per_day_per_subject'
            )
        ]
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class TotalClassCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="totalclasses")
    at_class = models.CharField(max_length=5)
    subject = models.ForeignKey(Subject, null=True, blank=True, on_delete=models.SET_NULL)
    total_class_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"