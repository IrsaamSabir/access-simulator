from django.db import models

class Room(models.Model):
    name = models.CharField(primary_key=True, max_length=64)
    min_access_level = models.IntegerField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    cooldown_minutes = models.IntegerField()


class AccessLog(models.Model):
    emp_id = models.CharField(max_length=16, db_index=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    access_time = models.TimeField()
    granted = models.BooleanField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)