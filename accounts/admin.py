from django.contrib import admin
from . import models


admin.site.register(models.User)
admin.site.register(models.StudentProfile)
admin.site.register(models.StudentResult)
admin.site.register(models.StudentAttendance)
admin.site.register(models.TotalClassCount)
admin.site.register(models.Subject)
