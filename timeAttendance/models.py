from django.db import models

# Create your models here.

class EmployeeDetail(models.Model):
    employee_id = models.IntegerField()
    name = models.CharField(max_length=32)
    Gender = models.IntegerField()
    CustomizeID = models.IntegerField()
    img_name = models.CharField(max_length=500, null=True)
    department = models.CharField(max_length=500, null=True)
    branch = models.CharField(max_length=500, null=True)

class EmployeeAttendance(models.Model):
    employee_id = models.IntegerField()
    name = models.CharField(max_length=32)
    capture_time = models.CharField(max_length=200)
    capture_location = models.CharField(max_length=100, null=True, blank=True)
    EmployeeDetail = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE, null=True)

class TerminalDetails(models.Model):
    terminal_id = models.IntegerField(primary_key=True)
    terminal_ip = models.CharField(max_length=100)
    terminal_name = models.CharField(max_length=100)
