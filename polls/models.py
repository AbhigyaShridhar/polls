from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    picture = models.BinaryField(null=True, editable=True)

    def __str__(self):
        return self.username

class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False, related_name="started_by")
    content = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    expiry = models.DateTimeField(help_text="Format: YYYY-MM-DD HOURS:MINUTES:SECONDS, example - 2021-10-16 19:30:51", blank=True, null=True)
    active = models.BooleanField(default=True)
    public = models.BooleanField(default=False)
    voted = models.ManyToManyField(User)

    def __str__(self):
        return self.content

class Choice(models.Model):
    text = models.TextField()
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text
