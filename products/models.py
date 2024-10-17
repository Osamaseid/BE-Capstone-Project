from django.contrib.auth.models import AbstractUser
from django.db import models

# User Schema
class User(AbstractUser):
    email = models.EmailField(unique=True)  # Unique email field for the user
    is_buyer = models.BooleanField(default=False)  # Flag to indicate if the user is a buyer
    is_seller = models.BooleanField(default=False)  # Flag to indicate if the user is a seller
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the user is created

    # Set unique related names to avoid clashes with default user groups/permissions
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",  # Unique related name for groups
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",  # Unique related name for permissions
        blank=True,
        help_text="Specific permissions for this user.",
    )

# Category Schema
class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category
    description = models.TextField(blank=True, null=True)  # Optional description of the category

    def __str__(self):
        return self.name  # String representation of the category

# Product Schema
class Product(models.Model):
    name = models.CharField(max_length=255)  # Name of the product
    description = models.TextField(blank=True, null=True)  # Optional description of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product
    stock_quantity = models.IntegerField()  # Quantity of product in stock
    image_url = models.URLField(max_length=255, blank=True, null=True)  # Optional URL for product image
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"  # Link to the Category model
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the product is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the product details are last updated
  
    def __str__(self):
        return self.name  # String representation of the product

# Review Schema
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')  # Link to the User model
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"  # Link to the Product model
    )
    rating = models.IntegerField()  # Rating given by the user
    comment = models.TextField(blank=True, null=True)  # Optional comment by the user
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the review is created

# Order Schema
class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),  # Order is pending
        ("shipped", "Shipped"),  # Order has been shipped
        ("delivered", "Delivered"),  # Order has been delivered
        ("cancelled", "Cancelled"),  # Order has been cancelled
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')  # Link to the User model
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")  # Current status of the order
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Total price of the order
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the order is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the order details are last updated

    def __str__(self):
        return f'Order {self.id} - {self.status}'  # String representation of the order

# Order Items Schema
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"  # Link to the Order model
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"  # Link to the Product model
    )
    quantity = models.IntegerField()  # Quantity of the product in this order item
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit of the product

    def __str__(self):
        return self.product.name  # String representation of the order item (product name)