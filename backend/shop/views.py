from rest_framework import generics,serializers
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import *
from user.models import User
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
import stripe


stripe.api_key=settings.STRIPE_SECRET_KEY

class StoreCreateView(generics.CreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [AllowAny]  #IsAuthenticated

    def perform_create(self, serializer):
        user=User.objects.get(id=1)   #remove this line
        if Store.objects.filter(owner=user).exists():  #  add self.request.user when adding frontend
            raise serializers.ValidationError({"error": "You already own a shop."})
        serializer.save(owner=user)  # add self.request.user


class StoreDetailView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [AllowAny] #IsAuthenticated


class StockCreateView(generics.CreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [AllowAny] #IsAuthenticated

    def perform_create(self, serializer):
        user=User.objects.get(id=1)   #remove this line
        store = Store.objects.filter(owner=user).first()  #add here self.request.user
        if not store:
            return Response({"error": "You do not own a store."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(store=store)


class StockListView(generics.ListAPIView):
    serializer_class = StockSerializer
    permission_classes = [AllowAny] #IsAuthenticated

    def get_queryset(self):
        user=User.objects.get(id=1)   #remove this line
        store = Store.objects.filter(owner=user).first() # add self.request.user
        if not store:
            return Stock.objects.none()  
        return Stock.objects.filter(store=store)



class ShopOrderCreateView(generics.CreateAPIView):
    queryset = ShopOrder.objects.all()
    serializer_class = ShopOrderSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        institute_request = serializer.validated_data.get("institute_request")
        store = serializer.validated_data.get("store")

        if ShopOrder.objects.filter(institute_request=institute_request).exists():
            raise serializers.ValidationError({"error": "This request has already been assigned to a shop."})

        total_amount = serializer.validated_data.get("total_amount")

        shop_order = serializer.save(status="pending", payment_status="pending")

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "inr",
                            "product_data": {
                                "name": f"Order {shop_order.id} - {store.name}",
                            },
                            "unit_amount": int(total_amount * 100),  
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=f"{settings.FRONTEND_URL}/payment-success/{shop_order.id}/{{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.FRONTEND_URL}/payment-failed/{shop_order.id}/{{CHECKOUT_SESSION_ID}}",
            )
            payment_link = checkout_session.url
            print(payment_link)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {"message": "Order created successfully", "order_id": shop_order.id, "payment_link": payment_link},
            status=status.HTTP_201_CREATED,
        )
    
class PaymentSuccessView(APIView):  
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):  
        payload = request.data

        store_id = payload.get("store_id")
        session_id = payload.get("session_id")

        shop_order = get_object_or_404(ShopOrder, id=store_id)

        if session_id and session_id != "null":
            session = stripe.checkout.Session.retrieve(session_id)

            if session.payment_status == "paid":
                if shop_order.payment_status == "pending":
                    shop_order.mark_paid()  
                    shop_order.complete_order()

                    return Response({"message": "Payment Successful"})
                else:
                    return Response({"message": "Already paid"})

            elif session.payment_status == "unpaid":
                return Response({"message": "Your invoice is unpaid"})

            elif session.payment_status == "cancelled":
                return Response({"message": "Your invoice is cancelled"})

            return Response({"message": "An error occurred. Try again"})

        return Response({"error": "Invalid session ID"}, status=400)
