from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)


class Employee(models.Model):
    name = models.CharField('Name', max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    salary = models.PositiveBigIntegerField()
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
