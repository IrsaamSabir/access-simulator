from rest_framework.views import APIView
from rest_framework.response import Response
from core.serializers import EmployeeReqSerializer
from core.mainlogic import simulate_batch

class SimulateAccessView(APIView):
    def post(self, request):
        serializer = EmployeeReqSerializer(data=request.data.get("employees", []), many=True)
        serializer.is_valid(raise_exception=True)
        results = simulate_batch(serializer.validated_data)
        return Response(results)


