# Postman Testing Guide for Profile API

## Base URL
```
http://192.168.32.1:8000
```

## Profile API Endpoint: `/api/profile/`

### 1. GET Profile (Retrieve Profile Information)

**Method:** `GET`
**URL:** `http://192.168.32.1:8000/api/profile/`
**Parameters:** Add as Query Parameters
- `rider_id`: `12345678` (8-digit rider ID)

**Example URL:**
```
http://192.168.32.1:8000/api/profile/?rider_id=12345678
```

**Expected Response:**
```json
{
    "username": "john_doe",
    "email": "test@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "location": "New York",
    "rider_id": "12345678"
}
```

---

### 2. POST Profile (Update Profile Information)

**Method:** `POST`
**URL:** `http://192.168.32.1:8000/api/profile/`
**Headers:**
- `Content-Type`: `application/json`

**Body (JSON):**
```json
{
    "rider_id": "12345678",
    "first_name": "John Updated",
    "last_name": "Doe Updated",
    "location": "Los Angeles"
}
```

**Expected Response:**
```json
{
    "message": "Profile updated successfully",
    "data": {
        "username": "john_doe",
        "email": "test@example.com",
        "first_name": "John Updated",
        "last_name": "Doe Updated",
        "location": "Los Angeles",
        "rider_id": "12345678"
    }
}
```

---

### 3. PATCH Profile (Partial Update)

**Method:** `PATCH`
**URL:** `http://192.168.32.1:8000/api/profile/`
**Headers:**
- `Content-Type`: `application/json`

**Body (JSON) - Update only specific fields:**
```json
{
    "rider_id": "12345678",
    "location": "Chicago"
}
```

**Expected Response:**
```json
{
    "username": "john_doe",
    "email": "test@example.com",
    "first_name": "John Updated",
    "last_name": "Doe Updated",
    "location": "Chicago",
    "rider_id": "12345678"
}
```

---

## Testing Steps in Postman:

### Step 1: Get a Valid Rider ID
First, register a user or login to get a rider_id:

**Register User:**
```
POST http://192.168.32.1:8000/api/register/
Body:
{
    "email": "testuser@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User"
}
```
**Response will contain:** `rider_id`

### Step 2: Test GET Profile
```
GET http://192.168.32.1:8000/api/profile/?rider_id=YOUR_RIDER_ID
```

### Step 3: Test POST Profile Update
```
POST http://192.168.32.1:8000/api/profile/
Body:
{
    "rider_id": "YOUR_RIDER_ID",
    "first_name": "Updated First",
    "last_name": "Updated Last",
    "location": "Updated Location"
}
```

### Step 4: Test PATCH Profile Update
```
PATCH http://192.168.32.1:8000/api/profile/
Body:
{
    "rider_id": "YOUR_RIDER_ID",
    "location": "New Location Only"
}
```

---

## Available Fields for Update:

### Updatable Fields:
- `first_name` (string)
- `last_name` (string)
- `location` (string, optional)

### Read-Only Fields:
- `username` (cannot be changed)
- `email` (cannot be changed via this endpoint)
- `rider_id` (system generated, cannot be changed)

---

## Error Responses:

### Missing Rider ID:
```json
{
    "error": "rider_id is required"
}
```

### Invalid Rider ID:
```json
{
    "error": "Invalid rider_id"
}
```

### Validation Errors:
```json
{
    "first_name": ["This field may not be blank."],
    "last_name": ["This field may not be blank."]
}
```

---

## Complete Test Collection for Postman:

### Collection: "Profile API Tests"

1. **Get Profile**
   - Method: GET
   - URL: `{{base_url}}/api/profile/?rider_id={{rider_id}}`

2. **Update Profile (POST)**
   - Method: POST
   - URL: `{{base_url}}/api/profile/`
   - Body: JSON with rider_id and fields to update

3. **Partial Update Profile (PATCH)**
   - Method: PATCH
   - URL: `{{base_url}}/api/profile/`
   - Body: JSON with rider_id and specific fields

### Environment Variables:
- `base_url`: `http://192.168.32.1:8000`
- `rider_id`: `12345678` (replace with actual rider ID)

---

## Quick Test Script:

You can also use this curl command to test:

```bash
# GET Profile
curl -X GET "http://192.168.32.1:8000/api/profile/?rider_id=12345678"

# POST Profile Update
curl -X POST "http://192.168.32.1:8000/api/profile/" \
  -H "Content-Type: application/json" \
  -d '{
    "rider_id": "12345678",
    "first_name": "Updated Name",
    "last_name": "Updated Last",
    "location": "Updated Location"
  }'
```