from django.db import models
from django.contrib.auth.models import User



class Review(models.Model):
    value = models.CharField(max_length= 500)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length = 50)



class Consumer(models.Model):
    profile = models.ForeignKey(User, on_delete = models.CASCADE)
    number = models.CharField(max_length = 50)
    bio = models.CharField(max_length = 1000)
    rating = models.FloatField(max_length = 5)

    def __str__(self):
        return self.profile.username


class Worker(models.Model):
    profile = models.ForeignKey(User, on_delete = models.CASCADE)
    number = models.CharField(max_length = 50)
    bio = models.CharField(max_length = 1000)
    rating = models.FloatField(max_length = 5)
    cv = models.FileField(upload_to = 'files/')
    client_reviews = models.ManyToManyField(Review)
    
    class Meta:
        ordering = ('rating',)

    def __str__(self):
        name = self.profile.username
        return name

class Job(models.Model):
    name = models.CharField(max_length = 500)
    description = models.CharField(max_length = 500)
    workers = models.ManyToManyField(Worker, blank = True)

    def __str__(self):
        return self.name


class Problem(models.Model):
    description = models.CharField(max_length = 500)
    price_range = models.FloatField(max_length = 500)
    special_request = models.CharField(max_length = 500)
    creator = models.ForeignKey(Consumer, on_delete = models.CASCADE, null = True)
    job_type = models.ForeignKey(Job, on_delete = models.CASCADE, null = True)
    available = models.BooleanField(default = True)
    def __str__(self):
        return self.description

class Reciept(models.Model):
    work = models.ForeignKey(Problem, on_delete=models.CASCADE)
    employee = models.ForeignKey(Worker, on_delete=models.CASCADE)
    issuer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    price = models.FloatField(max_length= 1250, default = 0)
    done = models.BooleanField(default = False)
    seen = models.BooleanField(default = False)
    scheduled_date = models.DateTimeField(null=True, blank=True)

class Bids(models.Model):
    bidder = models.ForeignKey(Worker, on_delete = models.CASCADE)
    work = models.ForeignKey(Problem, on_delete = models.CASCADE)
    value = models.FloatField(max_length = 20000)
    seen = models.BooleanField(default = False)
    note = models.CharField(max_length = 1250, null = True)
    scheduled_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('value',)

class Notifications(models.Model):
    profile = models.ForeignKey(User, on_delete = models.CASCADE)
    value = models.CharField(max_length = 1250, null = True)
    model_id = models.IntegerField( null = True)
    seen = models.BooleanField(default = False)