from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError






class UserBase(AbstractUser):
    email = models.CharField(unique=True) 
    def save(self, *args, **kwargs):
        self.email = self.email.lower()  # Convert to lowercase
        super().save(*args, **kwargs)  # Call the parent's save() method
    is_company = models.BooleanField(null=False, default=False)
    # Add unique related_name for groups
    groups = models.ManyToManyField(Group, related_name='custom_user_set', null=True, blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', null=True, blank=True)

class Customer(models.Model):
    user = models.OneToOneField(UserBase, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(null=False)
    logo = models.ImageField(upload_to='customer_pictures/', default='Customer_profile.webp')


class Company(models.Model):
    user = models.OneToOneField(
        UserBase, on_delete=models.CASCADE, primary_key=True)
    logo = models.ImageField(upload_to='company_logos/', default='company_logos/default_logo.webp')
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
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            original_company = Company.objects.get(pk=self.pk)
            if original_company.field != self.field and self.field != 'All in One':
                self.service_set.all().delete()

        super().save(*args, **kwargs)
    

