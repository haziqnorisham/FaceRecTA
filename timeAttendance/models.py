from django.db import models

# Create your models here.
class EmployeeAttendance(models.Model):
    employee_id = models.IntegerField()
    name = models.CharField(max_length=32)
    capture_time = models.CharField(max_length=200)
    capture_location = models.CharField(max_length=100, null=True, blank=True)

class EmployeeDetail(models.Model):
    employee_id = models.IntegerField()
    name = models.CharField(max_length=32)
    Gender = models.IntegerField()
    CustomizeID = models.IntegerField()
    img_name = models.CharField(max_length=500, null=True)
