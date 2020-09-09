from django.conf import settings
from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User


class Post(models.Model):
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.CharField(max_length=144,null=True)
    title = models.CharField(max_length=200,null=True)
    location = models.TextField(default="Unknown")
    contents = models.TextField(null=True)
    categorized_contents = models.TextField(null=True)
    score = models.IntegerField(null=True)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title