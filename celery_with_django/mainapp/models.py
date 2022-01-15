from django.db import models


class Calculation(models.Model):
    """Track a calculation and its results"""
    
    OPERATIONS = (('SUM', 'sum'),('DIFF', 'diff'),('MULT', 'mult'),('DIV', 'div'),)

    
    STATUSES = (
        ('PENDING', 'Pending'),
        ('ERROR', 'Error'),
        ('SUCCESS', 'Success'),
    )

    oper = models.CharField(max_length=5, choices=OPERATIONS)
    input1 = models.IntegerField()
    input2 = models.IntegerField()
    output = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUSES)
    message = models.CharField(max_length=110, blank=True)


class Fruit(models.Model):
    name = models.CharField(max_length = 100)
    colour = models.CharField(max_length = 100)

    class Meta:
        db_table = "Fruit"

    def __str__(self):
        return self.name +" - "+ self.colour