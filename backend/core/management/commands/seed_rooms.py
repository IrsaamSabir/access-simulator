from django.core.management.base import BaseCommand
from core.models import Room

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        data = [
            {"name":"ServerRoom","min_access_level":2,"open_time":"09:00","close_time":"11:00","cooldown_minutes":15},
            {"name":"Vault","min_access_level":3,"open_time":"09:00","close_time":"10:00","cooldown_minutes":30},
            {"name":"R&D Lab","min_access_level":1,"open_time":"08:00","close_time":"12:00","cooldown_minutes":10},
        ]
        for r in data:
            Room.objects.update_or_create(name=r["name"], defaults=r)
        self.stdout.write(self.style.SUCCESS("Rooms seeded"))
