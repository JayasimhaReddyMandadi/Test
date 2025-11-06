# Postman Guide for Change Email API

## Base URL: `http://192.168.32.1:8000`

---

## Change Email API

### **API Details:**
- **URL:** `http://192.168.32.1:8000/api/profile/change-email/`
- **Method:** `POST`
- **Purpose:** Update user's email address

### **Required Fields:**
- `rider_id` (string) - 8-digit rider ID
- `new_email` (string) - New email address
- `current_password` (string) - Current password for verification

---

## Postman Setup

### **Step 1: Configure Request**
1. **Method:** Select `POST`
2. **URL:** `http://192.168.32.1:8000/api/profile/change-email/`
3. **Headers:** 
   - Key: `Content-Type`
   - Value: `application/json`

### **Step 2: Request Body**
4. **Body:** Select `raw` and `JSON`
   ```json
   {
       "rider_id": "12345678",
       "new_email": "newemail@example.com",
       "current_password": "currentpassword123"
   }
   ```

### **Step 3: Send Request**
5. **Click Send**

---

## Expected Responses

### **Success Response:**
```json
{
    "message": "Email updated successfully",
    "email": "newemail@example.com"
}
```

### **Error Responses:**

#### **Missing rider_id:**
```json
{
    "error": "rider_id is required"
}
```

#### **Invalid rider_id:**
```json
{
    "error": "Invalid rider_id"
}
```

#### **Incorrect password:**
```json
{
    "current_password": ["Incorrect password."]
}
```

#### **Email already in use:**
```json
{
    "new_email": ["This email is already in use."]
}
```

#### **Missing required fields:**
```json
{
    "new_email": ["This field is required."],
    "current_password": ["This field is required."]
}
```

#### **Invalid email format:**
```json
{
    "new_email": ["Enter a valid email address."]
}
```

---

## Complete Test Scenarios

### **Scenario 1: Successful Email Change**
```json
POST /api/profile/change-email/
{
    "rider_id": "12345678",
    "new_email": "updated@example.com",
    "current_password": "correctpassword123"
}
```
**Expected:** Success message with new email

### **Scenario 2: Wrong Password**
```json
POST /api/profile/change-email/
{
    "rider_id": "12345678",
    "new_email": "updated@example.com",
    "current_password": "wrongpassword"
}
```
**Expected:** Error about incorrect password

### **Scenario 3: Email Already Exists**
```json
POST /api/profile/change-email/
{
    "rider_id": "12345678",
    "new_email": "existing@example.com",
    "current_password": "correctpassword123"
}
```
**Expected:** Error about email already in use

### **Scenario 4: Invalid Email Format**
```json
POST /api/profile/change-email/
{
    "rider_id": "12345678",
    "new_email": "invalid-email",
    "current_password": "correctpassword123"
}
```
**Expected:** Error about invalid email format

### **Scenario 5: Missing Fields**
```json
POST /api/profile/change-email/
{
    "rider_id": "12345678"
}
```
**Expected:** Error about required fields

---

## Testing Workflow

### **Step 1: Get Test User Credentials**
First, register a user or use existing credentials:
```json
POST /api/register/
{
    "email": "testuser@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
}
```
**Note the rider_id from response**

### **Step 2: Test Email Change**
Use the rider_id and password from Step 1:
```json
POST /api/profile/change-email/
{
    "rider_id": "YOUR_RIDER_ID",
    "new_email": "newemail@example.com",
    "current_password": "testpass123"
}
```

### **Step 3: Verify Email Changed**
Check if email was updated by getting personal info:
```json
POST /api/personal-info/
{
    "rider_id": "YOUR_RIDER_ID"
}
```
**Should show the new email**

### **Step 4: Test Login with New Email**
Try logging in with the new email:
```json
POST /api/login/
{
    "email": "newemail@example.com",
    "password": "testpass123"
}
```
**Should work with new email**

---

## Important Notes

⚠️ **Security Features:**
- Requires current password for verification
- Checks if new email is already in use
- Validates email format
- Updates both User model and RiderInfo table

✅ **What Gets Updated:**
- User.email field in database
- RiderInfo.email field (if exists)
- User can login with new email

❌ **What Doesn't Change:**
- rider_id remains the same
- username remains the same
- password remains the same

---

## Troubleshooting

### **Common Issues:**

1. **"rider_id is required"**
   - Make sure rider_id is included in request body
   - Check that rider_id is a string, not number

2. **"Invalid rider_id"**
   - Verify the rider_id exists in database
   - Check for typos in rider_id

3. **"Incorrect password"**
   - Verify you're using the correct current password
   - Password is case-sensitive

4. **"This email is already in use"**
   - Try a different email address
   - Check if email exists in system

5. **"Enter a valid email address"**
   - Check email format (must include @ and domain)
   - Remove extra spaces

---

## Sample Postman Collection

### Collection: "Change Email API Test"

1. **Register User**
   - Method: POST
   - URL: `{{base_url}}/api/register/`

2. **Change Email - Success**
   - Method: POST
   - URL: `{{base_url}}/api/profile/change-email/`

3. **Change Email - Wrong Password**
   - Method: POST
   - URL: `{{base_url}}/api/profile/change-email/`

4. **Verify Email Changed**
   - Method: POST
   - URL: `{{base_url}}/api/personal-info/`

### Environment Variables:
- `base_url`: `http://192.168.32.1:8000`
- `rider_id`: `12345678` (replace with actual)
- `current_password`: `testpass123` (replace with actual)