from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Product, Category, Order, OrderItem, Review
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

# User model (using Django's get_user_model for flexibility)
User = get_user_model()

# User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2", "is_buyer", "is_seller")

    def validate(self, attrs):
        # Ensure that the two password fields match
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        # Create a new user instance with the validated data
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            is_buyer=validated_data.get("is_buyer", False),
            is_seller=validated_data.get("is_seller", False),
        )
        # Hash the password before saving
        user.set_password(validated_data["password"])
        user.save()
        return user

# User Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            # Authenticate user credentials
            user = authenticate(username=username, password=password)
            if user:
                data['user'] = user  # Add the user to the validated data
            else:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Must provide both username and password.")

        return data

# Basic User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username")  # Expose only essential fields

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]  # Serialize fields for category

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # Link to Category model

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "stock_quantity",
            "image_url",
            "created_at",
        ]  # Serialize product fields

# Review Serializer
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username instead of user id

    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "comment", "created_at"]  

# Order Item Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Nest ProductSerializer for detailed product info

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "unit_price"] 

# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)  # Nest OrderItemSerializer

    class Meta:
        model = Order
        fields = [
            "__all__"  # Serialize all fields; consider specifying fields for clarity
        ]

# User Model in Order (if needed, you could expand on user details in the OrderSerializer)
class UserDetailInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]  # Serialize essential user details for orders