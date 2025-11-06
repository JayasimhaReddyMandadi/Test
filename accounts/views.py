from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.db.models import Sum, DecimalField
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from rest_framework import views, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import requests


from .models import Income, Expense, MutualFund, Profile, RiderInfo
from .serializers import UserSerializer, IncomeSerializer, ExpenseSerializer,MutualFundSerializer,UserProfileSerializer,ChangeEmailSerializer,ChangePasswordSerializer

# Helper function to get user by rider_id
def get_user_by_rider_id(rider_id):
    try:
        profile = Profile.objects.get(rider_id=rider_id)
        return profile.user
    except Profile.DoesNotExist:
        return None


# --- Register API ---
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        
        # Check if email already exists
        if email and User.objects.filter(email=email).exists():
            return Response({
                'error': 'Email already exists. Please try another email address.',
                'field': 'email'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                profile = user.profile  # This will be created by the signal
                return Response({
                    'message': 'User registered successfully',
                    'rider_id': profile.rider_id,
                    'user_id': user.pk,
                    'username': user.username,
                    'email': user.email
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': 'Registration failed. Please try again.',
                    'details': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Handle serializer errors with more specific messages
        errors = {}
        for field, field_errors in serializer.errors.items():
            if field == 'email':
                errors[field] = 'Please enter a valid email address.'
            elif field == 'password':
                errors[field] = 'Password is required and must be valid.'
            elif field == 'username':
                errors[field] = 'Username already exists. Please try another.'
            else:
                errors[field] = field_errors
        
        return Response({
            'error': 'Registration failed. Please check the details below.',
            'field_errors': errors
        }, status=status.HTTP_400_BAD_REQUEST)


# --- Login API ---
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Find the user by their email address first.
            user_obj = User.objects.get(email=email)
            
            # Now, authenticate using the found user's username and the provided password.
            user = authenticate(username=user_obj.username, password=password)
            
            if user is not None:
                profile = user.profile
                return Response({
                    'message': 'Login successful',
                    'rider_id': profile.rider_id,
                    'user_id': user.pk,
                    'username': user.username
                })
            else:
                # This case handles correct email but incorrect password.
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            # This case handles an email that doesn't exist in the database.
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        except User.MultipleObjectsReturned:
            # This is an edge case if emails are not unique in your database.
            # The first user found will be used for authentication attempt.
            user_obj = User.objects.filter(email=email).first()
            user = authenticate(username=user_obj.username, password=password)
            if user is not None:
                profile = user.profile
                return Response({
                    'message': 'Login successful',
                    'rider_id': profile.rider_id,
                    'user_id': user.pk,
                    'username': user.username
                })
            else:
                 return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(views.APIView):
    permission_classes = [AllowAny]
    # Add parsers to handle JSON, file uploads, and form data
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to fetch the user's combined profile data.
        """
        rider_id = request.GET.get('rider_id')
        if not rider_id:
            return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_by_rider_id(rider_id)
        if not user:
            return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to update user profile info.
        """
        rider_id = request.data.get('rider_id')
        if not rider_id:
            return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_by_rider_id(rider_id)
        if not user:
            return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
        
        # We pass request.data directly, which can include files
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """
        Handles PATCH requests to update user info, including file uploads.
        """
        rider_id = request.data.get('rider_id')
        if not rider_id:
            return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_by_rider_id(rider_id)
        if not user:
            return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
        
        # We pass request.data directly, which can include files
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name='dispatch')
class ChangeEmailView(views.APIView):
    """
    This is the API endpoint for changing the user's email.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        rider_id = request.data.get('rider_id')
        if not rider_id:
            return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_by_rider_id(rider_id)
        if not user:
            return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create a modified request context for the serializer
        modified_request = type('obj', (object,), {'user': user})()
        
        # Use the serializer to validate the data from the frontend
        serializer = ChangeEmailSerializer(data=request.data, context={'request': modified_request})
        
        if serializer.is_valid():
            # Get the new email from the validated data
            new_email = serializer.validated_data['new_email']
            
            # --- THIS IS WHERE THE DATABASE IS UPDATED ---
            user.email = new_email
            user.save() # This command saves the change to the database
            
            # Also update RiderInfo if it exists
            try:
                rider_info = user.rider_info
                rider_info.email = new_email
                rider_info.save()
            except RiderInfo.DoesNotExist:
                pass
            # ---------------------------------------------
            
            return Response({"message": "Email updated successfully", "email": user.email}, status=status.HTTP_200_OK)
        
        # If validation fails, send back the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name='dispatch')
class ChangePasswordView(views.APIView):
    """
    This is the API endpoint for changing the user's password.
    """
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        rider_id = request.data.get('rider_id')
        if not rider_id:
            return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_by_rider_id(rider_id)
        if not user:
            return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
        
        # Create a modified request context for the serializer
        modified_request = type('obj', (object,), {'user': user})()
        
        # Use the serializer to validate the old and new password data
        serializer = ChangePasswordSerializer(data=request.data, context={'request': modified_request})
        
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            
            # --- THIS IS WHERE THE DATABASE IS SECURELY UPDATED ---
            # user.set_password() handles the hashing for security
            user.set_password(new_password)
            user.save() # This command saves the change to the database
            # --------------------------------------------------------
            
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        
        # If validation fails, the serializer sends back the specific error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name='dispatch')
class DeleteAccountView(views.APIView):
    """
    This is the API endpoint for permanently deleting a user account.
    """
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        rider_id = request.data.get('rider_id')
        if not rider_id:
            return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_user_by_rider_id(rider_id)
        if not user:
            return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
        
        # --- THIS IS WHERE THE USER AND ALL THEIR DATA ARE DELETED ---
        user.delete()
        # -----------------------------------------------------------
        
        # Return a success message with a "204 No Content" status,
        # which is the standard for a successful deletion.
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# --- Add Income API ---
@api_view(['POST'])
@permission_classes([AllowAny])
def add_income(request):
    rider_id = request.data.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = IncomeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response({
            "message": "Income added successfully!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_expense(request):
    rider_id = request.data.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response({
            "message": "Expense added successfully!",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_data(request):
    rider_id = request.GET.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)

    total_income = user.incomes.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = user.expenses.aggregate(total=Sum('amount'))['total'] or 0
    total_saving = total_income - total_expense
    balance = total_saving  # can customize if needed

    return Response({
        "total_income": total_income,
        "total_expense": total_expense,
        "total_saving": total_saving,
        "balance": balance
    })

# --- Recent Transactions API ---
@api_view(['GET'])
@permission_classes([AllowAny])
def recent_transactions(request):
    rider_id = request.GET.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)

    incomes = Income.objects.filter(user=user).order_by('-date')[:5]
    expenses = Expense.objects.filter(user=user).order_by('-date')[:5]

    income_serializer = IncomeSerializer(incomes, many=True)
    expense_serializer = ExpenseSerializer(expenses, many=True)

    # Merge and sort by date descending
    transactions = income_serializer.data + expense_serializer.data
    transactions.sort(key=lambda x: x['date'], reverse=True)

    return Response({"transactions": transactions}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def add_fund_api(request):
    rider_id = request.data.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    serializer = MutualFundSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Funds List API
@api_view(['GET'])
@permission_classes([AllowAny])
def funds_list_api(request):
    rider_id = request.GET.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
    
    funds = MutualFund.objects.filter(user=user).order_by('-created_at')
    serializer = MutualFundSerializer(funds, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def update_fund_api(request, fund_id):
    rider_id = request.data.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        fund = MutualFund.objects.get(id=fund_id, user=user)
    except MutualFund.DoesNotExist:
        return Response({"error": "Fund not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MutualFundSerializer(fund, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_fund_api(request):
    """
    Deletes a mutual fund for the user using rider_id and fund_id from the JSON body.
    Example Request Body:
    {
        "rider_id": "R1234567",
        "fund_id": 1
    }
    """
    # Get the rider_id and fund_id from the JSON request body
    try:
        rider_id = request.data.get('rider_id')
        fund_id = request.data.get('fund_id')
    except AttributeError:
        return Response(
            {"error": "Invalid request body. JSON expected."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if both rider_id and fund_id were provided
    if not rider_id:
        return Response(
            {"error": "The 'rider_id' is required in the request body."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not fund_id:
        return Response(
            {"error": "The 'fund_id' is required in the request body."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Retrieve the fund by its ID and ensure it belongs to the user
        fund = MutualFund.objects.get(id=fund_id, user=user)
    except MutualFund.DoesNotExist:
        return Response({"error": "Fund not found."}, status=status.HTTP_404_NOT_FOUND)
    except (ValueError, TypeError):
        return Response({"error": "Invalid fund_id format provided."}, status=status.HTTP_400_BAD_REQUEST)

    # If the fund exists and belongs to the user, delete it
    fund.delete()
    
    return Response({"message": "Fund deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def portfolio_summary_api(request):
    rider_id = request.GET.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)

    # Get all funds for the current user
    user_funds = MutualFund.objects.filter(user=user)

    # Use the aggregate function to calculate sums efficiently in the database.
    # Coalesce is used to handle the case where a user has no funds, returning 0 instead of None.
    summary_data = user_funds.aggregate(
        total_invested=Coalesce(Sum('invested_amount'), 0, output_field=DecimalField()),
        total_current=Coalesce(Sum('current_value'), 0, output_field=DecimalField())
    )

    total_invested = summary_data['total_invested']
    total_current_value = summary_data['total_current']
    
    # Calculate derived values
    total_gain_loss = total_current_value - total_invested
    
    # Avoid division by zero if there are no investments
    if total_invested > 0:
        total_gain_loss_percentage = (total_gain_loss / total_invested) * 100
    else:
        total_gain_loss_percentage = 0

    # Prepare the final response data
    response_payload = {
        "total_invested": total_invested,
        "total_current_value": total_current_value,
        "total_gain_loss": total_gain_loss,
        "total_gain_loss_percentage": round(total_gain_loss_percentage, 2)
    }
    
    return Response(response_payload, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def market_data_api(request):
    """
    Acts as a proxy to fetch live market data for NSE indices.
    This view is designed to be robust and handle potential API failures gracefully.
    """
    NSE_URL = 'https://www.nseindia.com/api/allIndices'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response_data = {
        "marketStatus": "Unavailable", # Changed default from "Error"
        "nifty50": None,
        "nifty100": None,
        "bankNifty": None
    }

    try:
        # Fetch NSE Data
        nse_response = requests.get(NSE_URL, headers=HEADERS, timeout=5)
        nse_response.raise_for_status()
        nse_data = nse_response.json()
        
        response_data["marketStatus"] = nse_data.get("marketStatus", "Unavailable")

        # Helper to find an index by its exact name
        def find_index(data, index_name):
            return next((item for item in data if item.get("index") == index_name), None)

        nifty50_data = find_index(nse_data.get("data", []), "NIFTY 50")
        nifty100_data = find_index(nse_data.get("data", []), "NIFTY 100")
        bankNifty_data = find_index(nse_data.get("data", []), "NIFTY BANK")

        # Helper to format the index data
        def format_index_data(name, data):
            if not data: return None
            return {
                "name": name, "value": data["last"], "change": data["variation"],
                "percentChange": data["percentChange"], "open": data["open"],
                "high": data["high"], "low": data["low"], "prevClose": data["previousClose"]
            }

        response_data["nifty50"] = format_index_data("NIFTY 50", nifty50_data)
        response_data["nifty100"] = format_index_data("NIFTY 100", nifty100_data)
        response_data["bankNifty"] = format_index_data("NIFTY BANK", bankNifty_data)

    except requests.exceptions.RequestException as e:
        print(f"CRITICAL: Error fetching NSE data: {e}")
        # On failure, the marketStatus will remain "Unavailable"

    return Response(response_data, status=status.HTTP_200_OK)

def home(request):
    return JsonResponse({"message": "Welcome to the Expense Tracker API"})

# --- Personal Information APIs ---
@api_view(['POST'])
@permission_classes([AllowAny])
def get_personal_info(request):
    """
    API to get personal information (first_name, last_name, username, email)
    Pass rider_id in request body
    """
    rider_id = request.data.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'rider_id': rider_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def update_personal_info(request):
    """
    API to update personal information (first_name and last_name only)
    """
    rider_id = request.data.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
    
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    
    # Validate that at least one field is provided
    if not first_name and not last_name:
        return Response({
            'error': 'At least one field (first_name or last_name) is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Validate field lengths and content
    errors = {}
    if first_name is not None:
        if not first_name.strip():
            errors['first_name'] = 'First name cannot be empty'
        elif len(first_name.strip()) > 150:
            errors['first_name'] = 'First name cannot exceed 150 characters'
    
    if last_name is not None:
        if not last_name.strip():
            errors['last_name'] = 'Last name cannot be empty'
        elif len(last_name.strip()) > 150:
            errors['last_name'] = 'Last name cannot exceed 150 characters'
    
    if errors:
        return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
    
    # Update the user fields
    if first_name is not None:
        user.first_name = first_name.strip()
    if last_name is not None:
        user.last_name = last_name.strip()
    
    user.save()
    
    # Also update RiderInfo if it exists
    try:
        rider_info = user.rider_info
        rider_info.save()  # This will trigger the last_activity update
    except RiderInfo.DoesNotExist:
        pass
    
    return Response({
        'message': 'Personal information updated successfully',
        'data': {
            'rider_id': rider_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email
        }
    }, status=status.HTTP_200_OK)

# --- Get User Info by Rider ID API ---
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_info(request):
    rider_id = request.GET.get('rider_id')
    if not rider_id:
        return Response({'error': 'rider_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = get_user_by_rider_id(rider_id)
    if not user:
        return Response({'error': 'Invalid rider_id'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'rider_id': rider_id,
        'user_id': user.pk,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'date_joined': user.date_joined,
        'last_login': user.last_login
    }, status=status.HTTP_200_OK)

# --- Get All Riders (for admin purposes) ---
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_riders(request):
    """Get all riders with their basic info"""
    try:
        riders_info = RiderInfo.objects.select_related('user').all()
        riders_data = []
        
        for rider_info in riders_info:
            user = rider_info.user
            try:
                profile = user.profile
                location = profile.location
                profile_created = profile.created_at
            except Profile.DoesNotExist:
                location = ""
                profile_created = None
            
            riders_data.append({
                'rider_id': rider_info.rider_id,
                'user_id': user.pk,
                'username': rider_info.username,
                'email': rider_info.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined,
                'last_login': user.last_login,
                'location': location,
                'is_active': rider_info.is_active,
                'rider_created_at': rider_info.created_at,
                'last_activity': rider_info.last_activity
            })
        
        return Response({
            'total_riders': len(riders_data),
            'active_riders': len([r for r in riders_data if r['is_active']]),
            'riders': riders_data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- Get Rider by Email ---
@api_view(['GET'])
@permission_classes([AllowAny])
def get_rider_by_email(request):
    """Get rider information by email"""
    email = request.GET.get('email')
    if not email:
        return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        rider_info = RiderInfo.objects.select_related('user').get(email=email)
        user = rider_info.user
        
        return Response({
            'rider_id': rider_info.rider_id,
            'user_id': user.pk,
            'username': rider_info.username,
            'email': rider_info.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': rider_info.is_active,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'rider_created_at': rider_info.created_at,
            'last_activity': rider_info.last_activity
        }, status=status.HTTP_200_OK)
        
    except RiderInfo.DoesNotExist:
        return Response({'error': 'No rider found with this email'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# --- Verify Rider ID and Email Match ---
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_rider_email(request):
    """Verify that rider_id and email belong to the same user"""
    rider_id = request.data.get('rider_id')
    email = request.data.get('email')
    
    if not rider_id or not email:
        return Response({'error': 'Both rider_id and email are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        rider_info = RiderInfo.objects.get(rider_id=rider_id, email=email)
        return Response({
            'verified': True,
            'rider_id': rider_info.rider_id,
            'email': rider_info.email,
            'username': rider_info.username,
            'user_id': rider_info.user.pk
        }, status=status.HTTP_200_OK)
        
    except RiderInfo.DoesNotExist:
        return Response({
            'verified': False,
            'error': 'Rider ID and email do not match'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def login_page(request):
    return render(request, 'accounts/login.html')

def register_page(request):
    return render(request, 'accounts/register.html')

def profile_page(request):
    return render(request, 'accounts/ProfilePage.html')

def dashboard_selection_page(request):
    return render(request, 'accounts/dashboard_selection.html')

def daily_expense_dashboard_page(request):
    return render(request, 'accounts/DailyExpensiveDashboard.html')

def phonepay_gold_dashboard(request):
    return render(request, 'accounts/PhonePayGoldDashboard.html')

def mutualfund_dashboard(request):
    return render(request, 'accounts/mutual_fund_dashboard.html')