# Postman Guide for Delete Account API

## Base URL: `http://192.168.32.1:8000`

---

## Delete Account API

### **API Details:**
- **URL:** `http://192.168.32.1:8000/api/profile/delete-account/`
- **Method:** `POST`
- **Purpose:** Permanently delete user account and all associated data

### **⚠️ WARNING:**
This action is **PERMANENT** and **IRREVERSIBLE**. All user data including:
- Personal information
- Income records
- Expense records
- Mutual fund data
- Profile information
will be permanently deleted.

### **Required Fields:**
- `rider_id` (string) - 8-digit rider ID
- `current_password` (string) - Current password for verification

---

## Postman Setup

### **Step 1: Configure Request**
1. **Method:** Select `POST`
2. **URL:** `http://192.168.32.1:8000/api/profile/delete-account/`
3. **Headers:** 
   - Key: `Content-Type`
   - Value: `application/json`

### **Step 2: Request Body**
4. **Body:** Select `raw` and `JSON`
   ```json
   {
       "rider_id": "88788090",
       "current_password": "123456"
   }
   ```

### **Step 3: Send Request**
5. **Click Send**

---

## Expected Responses

### **Success Response:**
```json
{
    "message": "Account deleted successfully"
}
```
**Status Code:** 200 OK

### **Error Responses:**

#### **Missing rider_id:**
```json
{
    "error": "rider_id is required"
}
```
**Status Code:** 400 Bad Request

#### **Missing password:**
```json
{
    "error": "current_password is required for account deletion"
}
```
**Status Code:** 400 Bad Request

#### **Invalid rider_id:**
```json
{
    "error": "Invalid rider_id"
}
```
**Status Code:** 404 Not Found

#### **Incorrect password:**
```json
{
    "error": "Incorrect password. Account deletion cancelled."
}
```
**Status Code:** 401 Unauthorized

---

## Complete Test Scenarios

### **Scenario 1: Successful Account Deletion**
```json
POST /api/profile/delete-account/
{
    "rider_id": "88788090",
    "current_password": "123456"
}
```
**Expected:** Success message, account deleted

### **Scenario 2: Wrong Password**
```json
POST /api/profile/delete-account/
{
    "rider_id": "88788090",
    "current_password": "wrongpassword"
}
```
**Expected:** Error about incorrect password

### **Scenario 3: Missing Password**
```json
POST /api/profile/delete-account/
{
    "rider_id": "88788090"
}
```
**Expected:** Error about required password

### **Scenario 4: Missing rider_id**
```json
POST /api/profile/delete-account/
{
    "current_password": "123456"
}
```
**Expected:** Error about required rider_id

### **Scenario 5: Invalid rider_id**
```json
POST /api/profile/delete-account/
{
    "rider_id": "99999999",
    "current_password": "123456"
}
```
**Expected:** Error about invalid rider_id

---

## Testing Workflow

### **Step 1: Create Test Account**
First, register a test user:
```json
POST /api/register/
{
    "email": "deletetest@example.com",
    "password": "testpass123",
    "first_name": "Delete",
    "last_name": "Test"
}
```
**Note the rider_id from response**

### **Step 2: Add Some Data (Optional)**
Add income, expenses, or funds to verify all data is deleted:
```json
POST /api/income/add/
{
    "rider_id": "YOUR_RIDER_ID",
    "source": "Test Income",
    "amount": 1000,
    "date": "2024-11-04",
    "notes": "Test"
}
```

### **Step 3: Delete Account**
Use the rider_id and password from Step 1:
```json
POST /api/profile/delete-account/
{
    "rider_id": "YOUR_RIDER_ID",
    "current_password": "testpass123"
}
```

### **Step 4: Verify Account Deleted**
Try to login with deleted account:
```json
POST /api/login/
{
    "email": "deletetest@example.com",
    "password": "testpass123"
}
```
**Should fail with invalid credentials**

---

## Important Notes

⚠️ **Security Features:**
- Requires password verification before deletion
- Cannot be undone
- All related data is deleted (CASCADE)

✅ **What Gets Deleted:**
- User account
- Profile information
- RiderInfo record
- All income records
- All expense records
- All mutual fund records
- All related data

❌ **Cannot Be Recovered:**
- Once deleted, the account cannot be restored
- All data is permanently lost
- The rider_id becomes available for reuse

---

## Data Deletion Details

When an account is deleted, the following happens:

1. **User Model:** Deleted
2. **Profile Model:** Deleted (CASCADE)
3. **RiderInfo Model:** Deleted (CASCADE)
4. **Income Records:** All deleted (CASCADE)
5. **Expense Records:** All deleted (CASCADE)
6. **MutualFund Records:** All deleted (CASCADE)

The deletion is handled by Django's CASCADE delete, which automatically removes all related records.

---

## Troubleshooting

### **Common Issues:**

1. **"rider_id is required"**
   - Make sure rider_id is included in request body
   - Check JSON format is correct

2. **"current_password is required for account deletion"**
   - Include current_password in request body
   - Password field cannot be empty

3. **"Invalid rider_id"**
   - Verify the rider_id exists
   - Check for typos

4. **"Incorrect password. Account deletion cancelled."**
   - Verify you're using the correct password
   - Password is case-sensitive
   - Check for extra spaces

5. **404 Page Not Found**
   - Make sure URL is `/api/profile/delete-account/` (not `/api/delete-account/`)
   - Check method is POST (not DELETE)

---

## Sample Postman Collection

### Collection: "Delete Account API Test"

1. **Register Test User**
   - Method: POST
   - URL: `{{base_url}}/api/register/`

2. **Add Test Data**
   - Method: POST
   - URL: `{{base_url}}/api/income/add/`

3. **Delete Account - Success**
   - Method: POST
   - URL: `{{base_url}}/api/profile/delete-account/`
   - Body: Valid rider_id and password

4. **Delete Account - Wrong Password**
   - Method: POST
   - URL: `{{base_url}}/api/profile/delete-account/`
   - Body: Valid rider_id, wrong password

5. **Verify Account Deleted**
   - Method: POST
   - URL: `{{base_url}}/api/login/`
   - Body: Deleted account credentials

### Environment Variables:
- `base_url`: `http://192.168.32.1:8000`
- `rider_id`: `88788090` (replace with actual)
- `password`: `123456` (replace with actual)

---

## Quick Reference

### **Correct URL:**
```
POST http://192.168.32.1:8000/api/profile/delete-account/
```

### **Request Body:**
```json
{
    "rider_id": "88788090",
    "current_password": "123456"
}
```

### **Success Response:**
```json
{
    "message": "Account deleted successfully"
}
```

---

## Key Changes Made:

✅ **Changed from DELETE to POST method**
✅ **Added password verification** for security
✅ **Better error messages**
✅ **Consistent with other APIs**
✅ **Proper URL:** `/api/profile/delete-account/`