from django.db import models
from django.db.utils import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Todo(models.Model):
    title = models.CharField(max_length = 50, unique = True)
    desc = models.CharField(max_length = 3000)
    added = models.DateField()
    completed = models.DateField(default = None, blank = True, null = True)
    user = models.ForeignKey(User, default = 1, null = True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Todo '{}',\nby {}".format(self.title, self.user)
