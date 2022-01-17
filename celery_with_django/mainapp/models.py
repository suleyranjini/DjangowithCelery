from django.db import models


class Calculation(models.Model):
       
    oper = models.CharField(max_length=5)
    input1 = models.IntegerField()
    input2 = models.IntegerField()
    output = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=8,null=True)
    message = models.CharField(max_length=110, blank=True)

    def __str__(self):
        return self.message
    
    class Meta:
        db_table = "Calculation"


class Fruit(models.Model):
    name = models.CharField(max_length = 100)
    colour = models.CharField(max_length = 100)

    class Meta:
        db_table = "Fruit"

    def __str__(self):
        return self.name +" - "+ self.colour