from django.db import models
from users.models import Customer, Company
from django.core.validators import MinValueValidator, MaxValueValidator

class Service(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, primary_key=True)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], default=0)
    field = (
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
    )
    date = models.DateTimeField(auto_now=True, null=False)
    requests_count = models.IntegerField(default=0)


