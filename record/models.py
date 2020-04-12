from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Record(models.Model):
    DIFFICULTY_CHOICES = (
        (1, 'Beginner'), (2, 'Intermediate'), (3, 'Expert'), (4, 'Custom')
    )
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=2)
    finish_time = models.IntegerField(default=-1)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<Record: player: %s, time: %d>' % (self.player, self.finish_time)

    class Meta:
        db_table = 'record'
