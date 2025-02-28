from django.db import models
from user.models import User
from institute.models import InstituteRequest

class Store(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shop")
    name = models.CharField(max_length=255, unique=True)
    location = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    



class Stock(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="stocks")
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} - {self.store.name}"

class ShopOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="orders")
    institute_request = models.OneToOneField(
        InstituteRequest,  
        on_delete=models.CASCADE,
        related_name="shop_order"
    )
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_paid(self):
        self.payment_status = "paid"
        self.save()

    def complete_order(self):
        self.status = "completed"
        self.save()
        self.update_stock()

    def update_stock(self):
        ordered_items = self.order_items.all()  # we are decrementing this stock need to use these in algo.
        for item in ordered_items:
            item.product.stock.quantity -= item.quantity
            item.product.stock.save()

    def __str__(self):
        return f"Order {self.id} - {self.store.name} - {self.status}"


class ShopRating(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)]) 
    review = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
