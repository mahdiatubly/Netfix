from django.db import models
from star_ratings.models import Rating
from users.models import Customer, Company
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Service(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=100)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], default=0)
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

    def update_rating(self):
        completed_requests = Request.objects.filter(service=self, completed=True, rating__isnull=False)
        total_rating = completed_requests.aggregate(models.Avg('rating'))['rating__avg']
        self.rating = total_rating if total_rating is not None else 0
        self.save()

class Request(models.Model):
    id = models.AutoField(primary_key=True)
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True, null=False)
    completed = models.BooleanField(default=False)
    rating = models.IntegerField(validators=[MinValueValidator(
        0), MaxValueValidator(5)], null = True, blank = True)
    duration = models.IntegerField( default = 1 )
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.completed and self.rating is not None:
            self.service.update_rating()
            self.service.requests_count = Request.objects.filter(service=self.service, completed=True).count()
            self.service.save()

    def __str__(self):
        return str(self.id)


