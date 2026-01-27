from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField()

    RoleChoices = (
        ('buyer', 'buyer'),
        ('seller', 'seller')
    )
    user_role = models.CharField(max_length=20, choices=RoleChoices, default='buyer')
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Region(models.Model):
    region_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.region_name}'


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')
    city_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.city_name} {self.region.region_name}'


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')
    district_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.district_name} {self.city.city_name}'


class Property(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    HouseChoices = (
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Plot', 'Plot'),
        ('Cottage', 'Cottage'),
        ('Villa', 'Villa'),
    )

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='properties_region')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='properties_city')
    property_type = models.CharField(max_length=100, choices=HouseChoices)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='properties_district')

    address = models.CharField(max_length=300)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=20, decimal_places=2)

    total_floor = models.SmallIntegerField()
    floor = models.SmallIntegerField()

    ConditionChoices = (
        ('Europe', 'Europe'),
        ('Good', 'Good'),
        ("Need's repair", "Need's repair"),
    )
    condition = models.CharField(max_length=100, choices=ConditionChoices)

    documents = models.BooleanField()
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='properties_seller')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


    def get_avg_rating(self):
        reviews = self.hotel_review.all()
        if reviews.exists():
            return round(sum(i.rating for i in reviews) / reviews.count(), 1)
        return 0

    def get_count_people(self):
        return self.hotel_review.count()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_images')
    property_image = models.ImageField(upload_to='property_images')
    video = models.FileField(upload_to='property_videos')

    def __str__(self):
        return self.property.title


class Review(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reviews_left'
    )

    seller = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reviews_received'
        ,null=True, blank=True
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='home_review'
    )

    rating = models.PositiveSmallIntegerField(choices=[(n, str(n)) for n in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}, {self.property.title}'
