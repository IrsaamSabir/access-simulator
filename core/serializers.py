from rest_framework import serializers

class EmployeeReqSerializer(serializers.Serializer):
    id = serializers.CharField()
    access_level = serializers.IntegerField()
    request_time = serializers.TimeField(format="%H:%M", input_formats=["%H:%M"])
    room = serializers.CharField()