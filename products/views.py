from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from .models import Category, Product, Review, Order, OrderItem

User = get_user_model()

# User registration view
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()  # Queryset for all users
    serializer_class = RegisterSerializer  # Serializer for user registration
    permission_classes = [AllowAny]  # Allow any user to register

# Function to generate JWT tokens for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)  # Create refresh token for the user
    return {
        'refresh': str(refresh),  # Return refresh token as string
        'access': str(refresh.access_token),  # Return access token as string
    }

# User Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # Use the LoginSerializer

    def post(self, request,):
        serializer = self.get_serializer(data=request.data)  # Get data from request
        serializer.is_valid(raise_exception=True)  # Validate the data
        user = serializer.validated_data['user']  # Retrieve the authenticated user
        tokens = get_tokens_for_user(user)  # Get JWT tokens
    
        return Response({
            'user': UserSerializer(user).data,  # Return user details
            'tokens': tokens,  # Return JWT tokens
        })

# Get the authenticated user's details
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request,):
        serializer = UserSerializer(request.user)  # Serialize the current user
        return Response(serializer.data)  # Return user data


# Category Views
@permission_classes([IsAuthenticated])  # Require authentication for these views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()  # Queryset for all categories
    serializer_class = CategorySerializer  # Use the CategorySerializer

@permission_classes([IsAuthenticated])  # Require authentication
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()  # Queryset for all categories
    serializer_class = CategorySerializer  # Use the CategorySerializer


# Product Views
@permission_classes([IsAuthenticated])  # Require authentication
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()  # Queryset for all products
    serializer_class = ProductSerializer  # Use the ProductSerializer

@permission_classes([IsAuthenticated])  # Require authentication
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()  # Queryset for all products
    serializer_class = ProductSerializer  # Use the ProductSerializer


# Review Views
@permission_classes([IsAuthenticated])  # Require authentication
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()  # Queryset for all reviews
    serializer_class = ReviewSerializer  # Use the ReviewSerializer

    def perform_create(self, serializer):
        # Save the review with the current user as the reviewer
        serializer.save(user=self.request.user)

@permission_classes([IsAuthenticated])  # Require authentication
class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()  # Queryset for all reviews
    serializer_class = ReviewSerializer  # Use the ReviewSerializer


# Order Views
@permission_classes([IsAuthenticated])  # Require authentication
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()  # Queryset for all orders
    serializer_class = OrderSerializer  # Use the OrderSerializer

    def perform_create(self, serializer):
        # Save the order with the current user as the owner
        serializer.save(user=self.request.user)

@permission_classes([IsAuthenticated])  # Require authentication
class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()  # Queryset for all orders
    serializer_class = OrderSerializer  # Use the OrderSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated


# Order Item Views
@permission_classes([IsAuthenticated])  # Require authentication
class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()  # Queryset for all order items
    serializer_class = OrderItemSerializer  # Use the OrderItemSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

@permission_classes([IsAuthenticated])  # Require authentication
class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()  # Queryset for all order items
    serializer_class = OrderItemSerializer  # Use the OrderItemSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated