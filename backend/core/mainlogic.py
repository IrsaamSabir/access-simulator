from datetime import datetime
from core.models import Room, AccessLog


def minutes_diff(t1, t2):
    """Return difference in minutes between two time objects."""
    dt1 = datetime.combine(datetime.today(), t1)
    dt2 = datetime.combine(datetime.today(), t2)
    return (dt1 - dt2).total_seconds() / 60.0


def simulate_one(employee):
    emp_id = employee["id"]
    emp_level = employee["access_level"]
    req_time = employee["request_time"]  # datetime.time
    room_name = employee["room"]

    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return {"id": emp_id, "status": "Denied", "reason": "Room not found"}

    # Check access level
    if emp_level < room.min_access_level:
        AccessLog.objects.create(emp_id=emp_id, room=room,
                                 access_time=req_time, granted=False,
                                 reason="Denied: Below required level")
        return {"id": emp_id, "status": "Denied", "reason": "Denied: Below required level"}

    # Check room open/close (close_time exclusive)
    if not (room.open_time <= req_time < room.close_time):
        AccessLog.objects.create(emp_id=emp_id, room=room,
                                 access_time=req_time, granted=False,
                                 reason="Denied: Room closed")
        return {"id": emp_id, "status": "Denied", "reason": "Denied: Room closed"}

    # Check cooldown
    last_log = (
        AccessLog.objects.filter(emp_id=emp_id, room=room, granted=True)
        .order_by("-created_at")
        .first()
    )
    if last_log:
        diff = minutes_diff(req_time, last_log.access_time)
        if diff < room.cooldown_minutes:
            AccessLog.objects.create(emp_id=emp_id, room=room,
                                     access_time=req_time, granted=False,
                                     reason="Denied: Cooldown active")
            return {"id": emp_id, "status": "Denied", "reason": "Denied: Cooldown active"}

    # Grant access
    AccessLog.objects.create(emp_id=emp_id, room=room,
                             access_time=req_time, granted=True,
                             reason=f"Access granted to {room.name}")
    return {"id": emp_id, "status": "Granted", "reason": f"Access granted to {room.name}"}


def simulate_batch(employees):
    return [simulate_one(e) for e in employees]
