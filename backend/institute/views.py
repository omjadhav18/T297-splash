from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from .models import *
from user.models import User
from admapp.models import AdminRequestQueue
from .serializers import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView



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
                status="Pending",  
                added_at=timezone.now()
            )

        elif new_status == 'Rejected' and instance.status != 'Rejected':
            instance.rejected_at = timezone.now()
            instance.approved_at = None  

        instance.status = new_status
        instance.save()
        serializer.save()




class InstituteDocumentUploadView(generics.CreateAPIView):
    queryset = InstituteDocument.objects.all()
    serializer_class = InstituteDocumentSerializer
    permission_classes = [AllowAny] # Add IsAuthenticated

    def perform_create(self, serializer):
        #user = self.request.user
        user=User.objects.get(id=1)  # Make sure remove this line.
        if user.role != "institute":
            return Response({"error": "Only institutes can upload documents."}, status=403)

        if InstituteDocument.objects.filter(user=user).exists():
            return Response({"error": "You have already uploaded a document."}, status=400)

        serializer.save(user=user)


class InstituteDocumentReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, document_id):
        """Retrieve a document's details (Admin only)."""
        document = get_object_or_404(InstituteDocument, id=document_id)
        serializer = InstituteDocumentSerializer(document)
        return Response(serializer.data)

    def patch(self, request, document_id):
        """Update document status (Admin only)."""
        document = get_object_or_404(InstituteDocument, id=document_id)

        if request.user.role != "admin":
            return Response({"error": "Only admins can review documents."}, status=403)

        serializer = InstituteDocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(reviewed_at=timezone.now())
            return Response(serializer.data)
        return Response(serializer.errors, status=400)