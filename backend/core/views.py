from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.serializers import EmployeeReqSerializer
from core.mainlogic import simulate_batch


class SimulateAccessView(APIView):
    def post(self, request):
        employees = request.data.get("employees")
        if not employees:
            return Response({"detail": "No employees provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeReqSerializer(data=employees, many=True)
        serializer.is_valid(raise_exception=True)

        results = simulate_batch(serializer.validated_data)
        return Response({"results": results}, status=status.HTTP_200_OK)
