from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import *
from .serializers import DonationSerializer
from user.models import User
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class DonationListCreateView(generics.ListCreateAPIView):

    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user=User.objects.get(id=1)
        serializer.save(donor=user)  # add here self.request.user


class DonationDetailView(generics.RetrieveAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]




class DonationCreateView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        donation = serializer.save(payment_status="pending")  

        if donation.amount_donated is None or donation.amount_donated <= 0:
            return Response({"error": "Invalid donation amount"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"], 
                line_items=[
                    {
                        "price_data": {
                            "currency": "inr",
                            "product_data": {"name": f"Donation by {donation.donor.username if donation.donor else 'Anonymous'}"},
                            "unit_amount": int(donation.amount_donated * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=f"{settings.FRONTEND_URL}/donation-success/{donation.id}/{{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_URL}/donation-failed/{donation.id}/{{CHECKOUT_SESSION_ID}}",

            )
            payment_link = checkout_session.url
            print("Generated Payment Link:", payment_link)  
        except stripe.error.StripeError as e:
            print(f"Stripe Error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {
                "message": "Donation initiated successfully",
                "donation_id": donation.id,
                "payment_link": payment_link,
            },
            status=status.HTTP_201_CREATED,
        )
    


class DonationPaymentSuccessView(APIView):  
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):  
        payload = request.data

        donation_id = payload.get("donation_id")
        session_id = payload.get("session_id")

        donation = get_object_or_404(Donation, id=donation_id)

        if session_id and session_id != "null":
            try:
                session = stripe.checkout.Session.retrieve(session_id)

                if session.payment_status == "paid":
                    if donation.payment_status == "pending":
                        # Mark donation as paid
                        donation.payment_status = "Completed"  
                        donation.save()

                        # Create DonorPerson entry
                        DonorPerson.objects.create(
                            user=donation.donor,  
                            amount_donated=donation.amount_donated,
                            payment_status="Completed"
                        )

                        return Response({"message": "Donation Payment Successful"}, status=200)
                    else:
                        return Response({"message": "Already paid"}, status=200)

                elif session.payment_status == "unpaid":
                    return Response({"message": "Your donation is unpaid"}, status=400)

                elif session.payment_status == "cancelled":
                    return Response({"message": "Your donation was cancelled"}, status=400)

                return Response({"message": "An error occurred. Try again"}, status=400)

            except stripe.error.StripeError as e:
                return Response({"error": str(e)}, status=500)

        return Response({"error": "Invalid session ID"}, status=400)