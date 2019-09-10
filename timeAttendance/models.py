from django.db import models

# Create your models here.
class EmployeeAttendance(models.Model):
    employee_id = models.IntegerField()
    name = models.CharField(max_length=32)
    capture_time = models.CharField(max_length=200)

    def __str__(self):
        return self.employee_id
