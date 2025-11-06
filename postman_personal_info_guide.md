# Postman Guide for Personal Information APIs

## Base URL: `http://192.168.32.1:8000`

---

## 1. Get Personal Information

### **API Details:**
- **URL:** `http://192.168.32.1:8000/api/personal-info/`
- **Method:** `POST`
- **Purpose:** Get user's personal information

### **Postman Setup:**
1. **Method:** Select `POST`
2. **URL:** `http://192.168.32.1:8000/api/personal-info/`
3. **Headers:** 
   - Key: `Content-Type`
   - Value: `application/json`
4. **Body:** Select `raw` and `JSON`
   ```json
   {
       "rider_id": "12345678"
   }
   ```
5. **Click Send**

### **Expected Response:**
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

### **API Details:**
- **URL:** `http://192.168.32.1:8000/api/personal-info/update/`
- **Method:** `POST`
- **Purpose:** Update first name and last name

### **Postman Setup:**
1. **Method:** Select `POST`
2. **URL:** `http://192.168.32.1:8000/api/personal-info/update/`
3. **Headers:** 
   - Key: `Content-Type`
   - Value: `application/json`
4. **Body:** Select `raw` and `JSON`
   ```json
   {
       "rider_id": "12345678",
       "first_name": "Updated First",
       "last_name": "Updated Last"
   }
   ```
5. **Click Send**

### **Expected Response:**
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

## Test Scenarios

### **Scenario 1: Get Personal Info**
```json
POST /api/personal-info/
{
    "rider_id": "12345678"
}
```

### **Scenario 2: Update Both Names**
```json
POST /api/personal-info/update/
{
    "rider_id": "12345678",
    "first_name": "New First",
    "last_name": "New Last"
}
```

### **Scenario 3: Update Only First Name**
```json
POST /api/personal-info/update/
{
    "rider_id": "12345678",
    "first_name": "Only First Updated"
}
```

### **Scenario 4: Update Only Last Name**
```json
POST /api/personal-info/update/
{
    "rider_id": "12345678",
    "last_name": "Only Last Updated"
}
```

---

## Error Cases

### **Missing Rider ID:**
```json
{
    "error": "rider_id is required"
}
```

### **Invalid Rider ID:**
```json
{
    "error": "Invalid rider_id"
}
```

### **No Fields to Update:**
```json
{
    "error": "At least one field (first_name or last_name) is required"
}
```

### **Empty Names:**
```json
{
    "errors": {
        "first_name": "First name cannot be empty",
        "last_name": "Last name cannot be empty"
    }
}
```

---

## Quick Test Steps

1. **First, register a user to get rider_id:**
   ```
   POST /api/register/
   {
       "email": "test@example.com",
       "password": "testpass123",
       "first_name": "Test",
       "last_name": "User"
   }
   ```

2. **Use the returned rider_id for testing personal info APIs**

3. **Test get personal info:**
   ```
   POST /api/personal-info/
   {
       "rider_id": "YOUR_RIDER_ID"
   }
   ```

4. **Test update personal info:**
   ```
   POST /api/personal-info/update/
   {
       "rider_id": "YOUR_RIDER_ID",
       "first_name": "Updated Name",
       "last_name": "Updated Last"
   }
   ```

---

## Key Changes Made:

✅ **Both APIs now use POST method**
✅ **rider_id is passed in request body (not query parameter)**
✅ **Consistent request format across both APIs**
✅ **Same error handling and validation**