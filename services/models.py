from django.db import models
from users.models import Customer, Company, UserBase
from django.core.validators import MinValueValidator, MaxValueValidator

class Service(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], null = True, blank = True)
    field = models.CharField(max_length=70, choices=(
        ('Air Conditioner', 'Air Conditioner'),
        ('Carpentry', 'Carpentry'),
        ('Electricity', 'Electricity'),
        ('Gardening', 'Gardening'),
        ('Home Machines', 'Home Machines'),
        ('House Keeping', 'House Keeping'),
        ('Interior Design', 'Interior Design'),
        ('Locks', 'Locks'),
        ('Painting', 'Painting'),
        ('Plumbing', 'Plumbing'),
        ('Water Heaters', 'Water Heaters'),
    ), default='Air Conditioner')
    requests_count = models.IntegerField(default=0)

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    customer= models.OneToOneField(Customer, on_delete=models.CASCADE)
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, null=False)
    completed = models.BooleanField(default=False)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], null = True, blank = True) 
    def __str__(self):
        return str(self.id)



