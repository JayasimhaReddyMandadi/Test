from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Income,Expense,MutualFund


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User Registration.
    Username is now generated automatically on the backend.
    """
    # Username is now read-only as it will be generated from the name.
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']
    
    def validate_email(self, value):
        """
        Check that the email is not already in use.
        """
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email address is already registered. Please use a different email.")
        return value.lower()  # Store email in lowercase
    
    def validate_password(self, value):
        """
        Validate password strength.
        """
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value
    
    def validate(self, data):
        """
        Check that password and confirm_password match.
        """
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({
                "confirm_password": "Password and confirm password do not match."
            })
        return data
    
    def create(self, validated_data):
        """
        Custom create method to auto-generate a unique username.
        """
        # Remove confirm_password from validated_data as it's not needed for user creation
        validated_data.pop('confirm_password', None)
        
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        
        # Create a base username, e.g., "johnsmith"
        base_username = (first_name + last_name).lower().replace(' ', '')
        if not base_username:
            # Fallback for empty names
            base_username = "user"
            
        username = base_username
        counter = 1
        # Check for uniqueness and append a number if it exists
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Create the user with the guaranteed unique username
        user = User.objects.create_user(
            username=username,
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )
        return user
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Specify the fields to be returned and updated
        fields = ['username', 'email', 'first_name', 'last_name']
        # Make username and email read-only as they shouldn't be changed here
        read_only_fields = ['username', 'email','first_name','last_name']

class ChangeEmailSerializer(serializers.Serializer):
    """
    This serializer validates the data for the ChangeEmailView.
    """
    new_email = serializers.EmailField(required=True)
    current_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        # Check if the provided password is correct for the current user
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect password.")
        return value

    def validate_new_email(self, value):
        # Check if the new email is already being used by another account
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
class ChangePasswordSerializer(serializers.Serializer):
    """
    This serializer validates the data for the ChangePasswordView.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        # Rule 1: Check if the new password and its confirmation match
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "New passwords must match."})
        return data

    def validate_old_password(self, value):
        # Rule 2: Check if the old password provided is correct
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Your old password was entered incorrectly. Please enter it again.")
        return value


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'source', 'amount', 'date', 'notes', 'created_at']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'category', 'amount', 'date', 'notes', 'created_at']

class MutualFundSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutualFund
        fields = ['id', 'name', 'fund_type', 'invested_amount', 'current_value', 'created_at']