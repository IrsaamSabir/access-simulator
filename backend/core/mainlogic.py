from datetime import timedelta, datetime
from core.models import Room, AccessLog

def simulate_one(employee):
    emp_id = employee["id"]
    emp_level = employee["access_level"]
    req_time = employee["request_time"]
    room_name = employee["room"]

    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return {emp_id: "Room not found"}

    now_dt = datetime.combine(datetime.today(), req_time)

    if emp_level < room.min_access_level:
        return {emp_id: "Access Denied: insufficient level"}
    if not (room.open_time <= req_time <= room.close_time):
        return {emp_id: "Access Denied: room closed"}

    last_log = AccessLog.objects.filter(employee_id=emp_id, room=room, granted=True).order_by("-access_time").first()
    if last_log:
        cooldown = last_log.access_time + timedelta(minutes=room.cooldown_minutes)
        if now_dt < cooldown:
            return {emp_id: "Access Denied: cooldown active"}

    AccessLog.objects.create(employee_id=emp_id, room=room, granted=True, reason="OK")
    return {emp_id: "Access Granted"}

def simulate_batch(employees):
    results = {}
    for e in employees:
        results.update(simulate_one(e))
    return results
