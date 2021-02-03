from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    picture = models.ImageField(default='profiles/default.jpg', upload_to='profiles/')


class Hood(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    population = models.CharField(max_length=100)
    admin = models.ManyToManyField(User) 
    

    @classmethod
    def get_all_hoods(cls):
        return(Hood.objects.all())


class Business(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def filter_by_hood(cls,id):
        businesses = cls.objects.filter(hood_id = id)
        return businesses

    @classmethod
    def search_by_name(cls,search_term):
        businesses = cls.objects.filter(name__icontains=search_term)
        return businesses    

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def filter_by_hood(cls,id):
        news = cls.objects.filter(hood_id = id)
        return news



class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def filter_by_hood(cls,id):
        news = cls.objects.filter(hood_id = id)
        return news



class Profile(models.Model):
    name = models.CharField(max_length=50, default='')
    location = models.CharField(max_length=100, default='')
    reach = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE) 

   
class Meeting(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    venue = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def filter_by_hood(cls,id):
        meetings = cls.objects.filter(hood_id = id)
        return meetings



class Essential(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=50,blank=True)
    description = models.TextField()
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def filter_by_hood(cls,id):
        essentials = cls.objects.filter(hood_id = id)
        return essentials        
