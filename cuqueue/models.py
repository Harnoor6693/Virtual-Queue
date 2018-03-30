from django.db import models


class detail(models.Model):

    name=models.CharField(max_length=30)
    uid=models.CharField(max_length=30)
    mobile_no=models.BigIntegerField()
    email = models.EmailField(max_length=30)
    time=models.DateTimeField(auto_now=True)
    given_time=models.TimeField(auto_now=False)
    lineno=models.BigIntegerField()
    QR=models.ImageField()
    def __str__(self):
        return str(self.pk) + '.' +" "+  self.name