# Postman Guide for Change Password API

## Base URL: `http://192.168.32.1:8000`

---

## Change Password API

### **API Details:**
- **URL:** `http://192.168.32.1:8000/api/profile/change-password/`
- **Method:** `POST`
- **Purpose:** Update user's password

### **Required Fields:**
- `rider_id` (string) - 8-digit rider ID
- `old_password` (string) - Current password
- `new_password` (string) - New password
- `confirm_new_password` (string) - Confirm new password (must match new_password)

---

## Postman Setup

### **Step 1: Configure Request**
1. **Method:** Select `POST`
2. **URL:** `http://192.168.32.1:8000/api/profile/change-password/`
3. **Headers:** 
   - Key: `Content-Type`
   - Value: `application/json`

### **Step 2: Request Body**
4. **Body:** Select `raw` and `JSON`
   ```json
   {
       "rider_id": "12345678",
       "old_password": "currentpassword123",
       "new_password": "newpassword456",
       "confirm_new_password": "newpassword456"
   }
   ```

### **Step 3: Send Request**
5. **Click Send**

---

## Expected Responses

### **Success Response:**
```json
{
    "message": "Password updated successfully"
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

#### **Incorrect old password:**
```json
{
    "old_password": ["Your old password was entered incorrectly. Please enter it again."]
}
```

#### **Passwords don't match:**
```json
{
    "new_password": ["New passwords must match."]
}
```

#### **Missing required fields:**
```json
{
    "old_password": ["This field is required."],
    "new_password": ["This field is required."],
    "confirm_new_password": ["This field is required."]
}
```

---

## Complete Test Scenarios

### **Scenario 1: Successful Password Change**
```json
POST /api/profile/change-password/
{
    "rider_id": "12345678",
    "old_password": "oldpass123",
    "new_password": "newpass456",
    "confirm_new_password": "newpass456"
}
```
**Expected:** Success message

### **Scenario 2: Wrong Old Password**
```json
POST /api/profile/change-password/
{
    "rider_id": "12345678",
    "old_password": "wrongpassword",
    "new_password": "newpass456",
    "confirm_new_password": "newpass456"
}
```
**Expected:** Error about incorrect old password

### **Scenario 3: Passwords Don't Match**
```json
POST /api/profile/change-password/
{
    "rider_id": "12345678",
    "old_password": "oldpass123",
    "new_password": "newpass456",
    "confirm_new_password": "differentpass789"
}
```
**Expected:** Error about passwords not matching

### **Scenario 4: Missing Fields**
```json
POST /api/profile/change-password/
{
    "rider_id": "12345678",
    "old_password": "oldpass123"
}
```
**Expected:** Error about required fields

### **Scenario 5: Invalid rider_id**
```json
POST /api/profile/change-password/
{
    "rider_id": "99999999",
    "old_password": "oldpass123",
    "new_password": "newpass456",
    "confirm_new_password": "newpass456"
}
```
**Expected:** Error about invalid rider_id

---

## Testing Workflow

### **Step 1: Get Test User Credentials**
First, register a user:
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

### **Step 2: Test Password Change**
Use the rider_id and password from Step 1:
```json
POST /api/profile/change-password/
{
    "rider_id": "YOUR_RIDER_ID",
    "old_password": "testpass123",
    "new_password": "newpass456",
    "confirm_new_password": "newpass456"
}
```

### **Step 3: Verify Password Changed**
Try logging in with the new password:
```json
POST /api/login/
{
    "email": "testuser@example.com",
    "password": "newpass456"
}
```
**Should work with new password**

### **Step 4: Verify Old Password Doesn't Work**
Try logging in with the old password:
```json
POST /api/login/
{
    "email": "testuser@example.com",
    "password": "testpass123"
}
```
**Should fail with invalid credentials**

---

## Important Notes

⚠️ **Security Features:**
- Requires old password for verification
- New password must be confirmed
- Password is securely hashed before storage
- Old password becomes invalid immediately

✅ **What Gets Updated:**
- User password in database (hashed)
- User can login with new password
- Old password no longer works

❌ **What Doesn't Change:**
- rider_id remains the same
- username remains the same
- email remains the same
- All other user data remains unchanged

---

## Password Requirements

While the API doesn't enforce specific password requirements, consider these best practices:

✅ **Recommended:**
- Minimum 8 characters
- Mix of uppercase and lowercase
- Include numbers
- Include special characters

❌ **Avoid:**
- Common passwords (password123, etc.)
- Personal information
- Sequential characters (12345, abcde)

---

## Troubleshooting

### **Common Issues:**

1. **"rider_id is required"**
   - Make sure rider_id is included in request body
   - Check that rider_id is a string

2. **"Invalid rider_id"**
   - Verify the rider_id exists in database
   - Check for typos in rider_id

3. **"Your old password was entered incorrectly"**
   - Verify you're using the correct current password
   - Password is case-sensitive
   - Check for extra spaces

4. **"New passwords must match"**
   - Ensure new_password and confirm_new_password are identical
   - Check for typos
   - Check for extra spaces

5. **Login fails after password change**
   - Make sure you're using the NEW password
   - Clear any cached credentials
   - Try the test again

---

## Sample Postman Collection

### Collection: "Change Password API Test"

1. **Register User**
   - Method: POST
   - URL: `{{base_url}}/api/register/`
   - Body: Registration data

2. **Change Password - Success**
   - Method: POST
   - URL: `{{base_url}}/api/profile/change-password/`
   - Body: Valid password change data

3. **Change Password - Wrong Old Password**
   - Method: POST
   - URL: `{{base_url}}/api/profile/change-password/`
   - Body: Wrong old password

4. **Change Password - Passwords Don't Match**
   - Method: POST
   - URL: `{{base_url}}/api/profile/change-password/`
   - Body: Mismatched new passwords

5. **Login with New Password**
   - Method: POST
   - URL: `{{base_url}}/api/login/`
   - Body: New credentials

6. **Login with Old Password (Should Fail)**
   - Method: POST
   - URL: `{{base_url}}/api/login/`
   - Body: Old credentials

### Environment Variables:
- `base_url`: `http://192.168.32.1:8000`
- `rider_id`: `12345678` (replace with actual)
- `old_password`: `testpass123` (replace with actual)
- `new_password`: `newpass456` (replace with actual)

---

## Quick Reference

### **Successful Request:**
```json
{
    "rider_id": "12345678",
    "old_password": "current_password",
    "new_password": "new_password",
    "confirm_new_password": "new_password"
}
```

### **Success Response:**
```json
{
    "message": "Password updated successfully"
}
```

### **Common Errors:**
- Wrong old password → 400 with old_password error
- Passwords don't match → 400 with new_password error
- Missing fields → 400 with field errors
- Invalid rider_id → 404 with error message