from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAdminUser
from admapp.models import AdminRequestQueue
from admapp.serializers import AdminRequestQueueSerializer

class ApprovedRequestsAdminView(generics.ListAPIView):
    queryset = AdminRequestQueue.objects.all()
    serializer_class = AdminRequestQueueSerializer
    permission_classes = [AllowAny]  #Make sure add isAdminUser

    def get_queryset(self):
        return AdminRequestQueue.objects.filter(status="Approved")
