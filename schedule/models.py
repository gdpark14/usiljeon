from django.db import models

# Create your models here.
class Content(models.Model):
    creator=models.CharField(max_length=50)
    creator_key=models.IntegerField()
    contact=models.TextField()

    title=models.CharField(max_length=50)
    department=models.CharField(max_length=50)

    reward=models.CharField(max_length=50)

    condition=models.TextField()
    detail=models.TextField()
    
    location=models.CharField(max_length=50)
    
    password=models.IntegerField()

class DateTime(models.Model):
    content=models.ForeignKey(Content,on_delete=models.CASCADE)
    date=models.DateField()
    starttime=models.TimeField()
    endtime=models.TimeField()
    day_of_week=models.IntegerField()
    isUsed=models.BooleanField(default=False)

class UserTemp(models.Model):
    name=models.CharField(max_length=50)
    major=models.CharField(max_length=50)
    num_student=models.CharField(max_length=50)
    num_phone=models.CharField(max_length=50)
    num_account=models.CharField(max_length=50)
    
    time_temp=models.OneToOneField(DateTime,on_delete=models.CASCADE)

    password=models.IntegerField()