from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .models import *
from user.models import User
from admapp.models import AdminRequestQueue
from .serializers import *

class ItemListCreateView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        user=User.objects.get(id=1)
        return Item.objects.filter(institute=user) #add self.request.user

    def perform_create(self, serializer):
        user=User.objects.get(id=1)
        serializer.save(institute=user)# add self.request.user

class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    permission_classes = [AllowAny] # Add IsAuthenticated ...

    def get_queryset(self):
        user=User.objects.get(id=1)
        return Item.objects.filter(institute=user)  # Add self.request.user here

class InstituteRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = InstituteRequestSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user=User.objects.get(id=1)
        return InstituteRequest.objects.filter(institute=user)# add self.request.user

    def perform_create(self, serializer):
        user=User.objects.get(id=1)
        serializer.save(institute=user)# add self.request.user


class InstituteRequestAdminListView(generics.ListAPIView):
    queryset = InstituteRequest.objects.all()
    serializer_class = InstituteRequestSerializer
    permission_classes = [AllowAny]  # IsAdminUser  add this at frontend connection

class InstituteRequestAdminUpdateView(generics.UpdateAPIView): #for this you need to pass the primary key or id to this .
    queryset = InstituteRequest.objects.all()
    serializer_class = InstituteRequestSerializer
    permission_classes = [AllowAny]  # IsAdminUser  add this at frontend connection

    def perform_update(self, serializer):
        instance = serializer.instance
        new_status = self.request.data.get("status", instance.status)

        if new_status == 'Approved' and instance.status != 'Approved':
            instance.approved_at = timezone.now()
            instance.rejected_at = None

            AdminRequestQueue.objects.create(
                institute_request=instance,
                status="Pending",  # Default status when added to queue
                added_at=timezone.now()
            )

        elif new_status == 'Rejected' and instance.status != 'Rejected':
            instance.rejected_at = timezone.now()
            instance.approved_at = None  

        instance.status = new_status
        instance.save()
        serializer.save()