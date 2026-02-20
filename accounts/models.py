from django.db import models
from django.contrib.auth.models import AbstractUser


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
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    CLASS_CHOICES = [(str(i), str(i)) for i in range(0, 11)]
    class_list = models.CharField(choices=CLASS_CHOICES, max_length=10, default='1')
    
    roll = models.CharField(max_length=10)
    
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

class StudentResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    semester = models.CharField(max_length=50)
    year = models.CharField(max_length=50)
    cgpa = models.CharField(max_length=5)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
     
class StudentAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_class_count = models.CharField(max_length=50)
    total_attendance_count = models.CharField(max_length=5)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"