from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import Group, Permission



class UserBase(AbstractUser):
    email = models.CharField(unique=True) 
    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Convert to lowercase
        super().save(*args, **kwargs)  # Call the parent's save() method
    is_company = models.BooleanField(null=False, default=False)
    # Add unique related_name for groups
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

class Customer(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(null=False)

class Company(models.Model):
    user = models.OneToOneField(
        UserBase, on_delete=models.CASCADE, primary_key=True)
    field = models.CharField(max_length=70, choices=(('Air Conditioner', 'Air Conditioner'),
                                                     ('All in One', 'All in One'),
                                                     ('Carpentry', 'Carpentry'),
                                                     ('Electricity',
                                                      'Electricity'),
                                                     ('Gardening', 'Gardening'),
                                                     ('Home Machines',
                                                      'Home Machines'),
                                                     ('House Keeping',
                                                      'House Keeping'),
                                                     ('Interior Design',
                                                      'Interior Design'),
                                                     ('Locks', 'Locks'),
                                                     ('Painting', 'Painting'),
                                                     ('Plumbing', 'Plumbing'),
                                                     ('Water Heaters', 'Water Heaters')), blank=False, null=False)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(0)], default=0)

