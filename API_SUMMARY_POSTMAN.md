# Complete API Summary for Postman Testing

## Base URL: `http://192.168.32.1:8000`

---

## 📋 All APIs Use POST Method

All APIs now consistently use **POST** method with `rider_id` in the request body.

---

## 1. Get Personal Information

**URL:** `POST /api/personal-info/`

**Body:**
```json
{
    "rider_id": "12345678"
}
```

**Response:**
```json
{
    "rider_id": "12345678",
    "first_name": "John",
    "last_name": "Doe",
    "username": "john_doe",
    "email": "john@example.com"
}
```

---

## 2. Update Personal Information

**URL:** `POST /api/personal-info/update/`

**Body:**
```json
{
    "rider_id": "12345678",
    "first_name": "Updated First",
    "last_name": "Updated Last"
}
```

**Response:**
```json
{
    "message": "Personal information updated successfully",
    "data": {
        "rider_id": "12345678",
        "first_name": "Updated First",
        "last_name": "Updated Last",
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```

---

## 3. Change Email

**URL:** `POST /api/profile/change-email/`

**Body:**
```json
{
    "rider_id": "12345678",
    "new_email": "newemail@example.com",
    "current_password": "currentpassword123"
}
```

**Response:**
```json
{
    "message": "Email updated successfully",
    "email": "newemail@example.com"
}
```

---

## 4. Change Password

**URL:** `POST /api/profile/change-password/`

**Body:**
```json
{
    "rider_id": "12345678",
    "old_password": "oldpassword123",
    "new_password": "newpassword456",
    "confirm_new_password": "newpassword456"
}
```

**Response:**
```json
{
    "message": "Password updated successfully"
}
```

---

## 5. User Registration

**URL:** `POST /api/register/`

**Body:**
```json
{
    "email": "test@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
}
```

**Response:**
```json
{
    "message": "User registered successfully",
    "rider_id": "12345678",
    "user_id": 1,
    "username": "test_user"
}
```

---

## 6. User Login

**URL:** `POST /api/login/`

**Body:**
```json
{
    "email": "test@example.com",
    "password": "testpass123"
}
```

**Response:**
```json
{
    "message": "Login successful",
    "rider_id": "12345678",
    "user_id": 1,
    "username": "test_user"
}
```

---

## 7. Add Income

**URL:** `POST /api/income/add/`

**Body:**
```json
{
    "rider_id": "12345678",
    "source": "Salary",
    "amount": 50000,
    "date": "2024-11-04",
    "notes": "Monthly salary"
}
```

---

## 8. Add Expense

**URL:** `POST /api/expense/add/`

**Body:**
```json
{
    "rider_id": "12345678",
    "category": "Groceries",
    "amount": 2500,
    "date": "2024-11-04",
    "notes": "Weekly shopping"
}
```

---

## 9. Get Dashboard Data

**URL:** `GET /api/dashboard/?rider_id=12345678`

**Alternative (if you want POST):**
**URL:** `POST /api/dashboard/`
**Body:** `{"rider_id": "12345678"}`

---

## 10. Add Mutual Fund

**URL:** `POST /api/funds/add/`

**Body:**
```json
{
    "rider_id": "12345678",
    "name": "SBI Bluechip Fund",
    "fund_type": "Equity",
    "invested_amount": 10000,
    "current_value": 11500
}
```

---

## Postman Collection Setup

### Headers for All POST Requests:
- `Content-Type: application/json`

### Environment Variables:
- `base_url`: `http://192.168.32.1:8000`
- `rider_id`: `12345678` (get from registration/login)

---

## Quick Test Flow

1. **Register User** → Get `rider_id`
2. **Login** → Verify `rider_id`
3. **Get Personal Info** → View current data
4. **Update Personal Info** → Change name
5. **Change Email** → Update email
6. **Change Password** → Update password
7. **Add Income/Expense** → Test financial features
8. **Add Mutual Fund** → Test investment features

---

## Common Error Responses

### Missing rider_id:
```json
{
    "error": "rider_id is required"
}
```

### Invalid rider_id:
```json
{
    "error": "Invalid rider_id"
}
```

### Validation Errors:
```json
{
    "field_name": ["Error message here"]
}
```

---

## Key Changes Made:

✅ **All profile APIs use POST method**
✅ **Consistent request format** (rider_id in body)
✅ **No more PUT method** for simplicity
✅ **rider_id is 8-digit number** (no "R" prefix)
✅ **All APIs require rider_id** for user identification

---

## Testing Priority Order:

1. ✅ Register → Get rider_id
2. ✅ Login → Verify credentials
3. ✅ Get Personal Info → Load data
4. ✅ Update Personal Info → Edit name
5. ✅ Change Email → Update email
6. ✅ Change Password → Update password
7. ✅ Financial APIs → Income/Expense
8. ✅ Investment APIs → Mutual Funds