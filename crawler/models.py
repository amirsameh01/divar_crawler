from django.db import models

city_choices =(('tehran', 'Tehran'),
        ('isfahan', 'Isfahan'),
        ('karaj', 'Karaj'))

#Todo: add search param field
class PhoneNumbers(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    search_param = models.CharField(max_length=20)
    city = models.CharField(choices=city_choices, max_length= 20)
    created_at = models.DateTimeField(auto_now_add=True)