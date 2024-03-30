from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta,datetime,time
from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator




# Create your models here.
# __________________________________________________________________________________________________________

class CustomUser(AbstractUser):
    user_type_choices=[
        ('users', 'users'),
        ('Busoperator' ,'Busoperator'),
        ('SuperAdmin' ,'SuperAdmin'),
    ]
    user_type=models.CharField(max_length=50,choices=user_type_choices,default='user')
    phone=models.CharField(max_length=10)

class SuperAdmin(CustomUser):
    name=models.CharField(max_length=50)
    email_address = models.EmailField(null=True, blank=True)
    phone_number = models.IntegerField( null=True)
    def _str_(self):
        return self.name 


class Busoperator(CustomUser):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    website = models.URLField(null=True)
    logo = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class users(CustomUser):
    name=models.CharField(max_length=50)
    date_of_birth = models.CharField(null=True,max_length=100)
    profile_picture = models.ImageField( null=True)
    address = models.CharField(max_length=255, blank=True)

   
    
# __________________________________________________________________________________________
class Category(models.Model):
    name=models.CharField(max_length=200)
    Busoperators = models.ForeignKey(Busoperator,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Buses(models.Model):
    name = models.CharField(max_length=200)
    Operator = models.ForeignKey(Busoperator, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField()
    price = models.IntegerField()
    description = models.CharField(max_length=500)
    capacity = models.IntegerField(null=True)
    boarding_point = models.CharField(max_length=500)
    boarding_time = models.TimeField()
    dropping_point = models.CharField(max_length=500)
    dropping_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    duration = models.DurationField(null=True, blank=True)  # Field to store duration
    
    def save(self, *args, **kwargs):
        self.duration = self.calculate_duration()
        super().save(*args, **kwargs)

    def calculate_duration(self):
        # Assuming the bus operates within the same day
        boarding_datetime = datetime.combine(datetime.today(), self.boarding_time)
        dropping_datetime = datetime.combine(datetime.today(), self.dropping_time)
        
        if dropping_datetime < boarding_datetime:
            dropping_datetime += timedelta(days=1)
        
        duration = dropping_datetime - boarding_datetime
        return duration
    
    def __str__(self):
        return self.name
        

class Offer(models.Model):
    bus=models.ForeignKey(Buses,on_delete=models.CASCADE,related_name="offer_price")
    busoperators = models.ForeignKey(Busoperator,on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    start_date=models.DateTimeField()
    due_date=models.DateTimeField()
    options=(
        ("active","active"),
        ("expired","expired")
    )
    offer_status=models.CharField(max_length=200,choices=options,default="active")
    
    
    @property
    def status(self):
        return "expired" if self.due_date < timezone.now() else "active"
    


class Review(models.Model):
    user=models.ForeignKey(users,on_delete=models.CASCADE)
    bus=models.ForeignKey(Buses,null=True,on_delete=models.SET_NULL)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=300)



class Reservation(models.Model):
    bus = models.ForeignKey(Buses, on_delete=models.CASCADE)
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=50)
    journey_date = models.DateField()
    reservation_time = models.DateTimeField(default=timezone.now)
    choice=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]
    reservation_status=models.CharField(max_length=100,choices=choice,default="Pending")
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('bus', 'journey_date','seat_number')

        

class Payment(models.Model):
    user= models.ForeignKey(users, on_delete=models.CASCADE,null=True)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_time = models.DateTimeField(default=timezone.now)
    choice=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]
    payment_status=models.CharField(max_length=50,choices=choice,default='Completed')




    
    

