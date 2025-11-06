# Personal Information API Guide

## Base URL
```
http://192.168.32.1:8000
```

## 1. Get Personal Information API

### **Endpoint:** `/api/personal-info/`
**Method:** `POST`
**Purpose:** Load first name, last name, username, and email for profile screen

### **Headers:**
- `Content-Type: application/json`

### **Body Parameters:**
- `rider_id` (required) - 8-digit rider ID

### **Request Example:**
```json
{
    "rider_id": "12345678"
}
```

### **Response Example:**
```json
{
    "rider_id": "12345678",
    "first_name": "John",
    "last_name": "Doe",
    "username": "john_doe",
    "email": "john@example.com"
}
```

### **Error Responses:**
```json
// Missing rider_id
{
    "error": "rider_id is required"
}

// Invalid rider_id
{
    "error": "Invalid rider_id"
}
```

---

## 2. Update Personal Information API

### **Endpoint:** `/api/personal-info/update/`
**Method:** `POST`
**Purpose:** Update first name and last name only (username and email are read-only)

### **Headers:**
- `Content-Type: application/json`

### **Body Parameters:**
- `rider_id` (required) - 8-digit rider ID
- `first_name` (optional) - New first name
- `last_name` (optional) - New last name

**Note:** At least one of `first_name` or `last_name` must be provided.

### **Request Example:**
```json
{
    "rider_id": "12345678",
    "first_name": "John Updated",
    "last_name": "Doe Updated"
}
```

### **Response Example:**
```json
{
    "message": "Personal information updated successfully",
    "data": {
        "rider_id": "12345678",
        "first_name": "John Updated",
        "last_name": "Doe Updated",
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```

### **Partial Update Example:**
```json
// Update only first name
{
    "rider_id": "12345678",
    "first_name": "John Only Updated"
}
```

### **Error Responses:**
```json
// Missing rider_id
{
    "error": "rider_id is required"
}

// Invalid rider_id
{
    "error": "Invalid rider_id"
}

// No fields provided
{
    "error": "At least one field (first_name or last_name) is required"
}

// Validation errors
{
    "errors": {
        "first_name": "First name cannot be empty",
        "last_name": "Last name cannot exceed 150 characters"
    }
}
```

---

## Postman Testing Steps

### Step 1: Get Personal Information

1. **Method:** POST
2. **URL:** `http://192.168.32.1:8000/api/personal-info/`
3. **Headers:** 
   - Key: `Content-Type`
   - Value: `application/json`
4. **Body (raw JSON):**
   ```json
   {
       "rider_id": "12345678"
   }
   ```
5. **Click Send**

### Step 2: Update Personal Information

1. **Method:** POST
2. **URL:** `http://192.168.32.1:8000/api/personal-info/update/`
3. **Headers:** 
   - Key: `Content-Type`
   - Value: `application/json`
4. **Body (raw JSON):**
   ```json
   {
       "rider_id": "12345678",
       "first_name": "Updated First",
       "last_name": "Updated Last"
   }
   ```
5. **Click Send**

---

## Complete Test Scenarios

### Scenario 1: Load Profile Data
```
POST /api/personal-info/
Body: {
    "rider_id": "12345678"
}
```
**Expected:** Returns current user information

### Scenario 2: Update Both Names
```
POST /api/personal-info/update/
Body: {
    "rider_id": "12345678",
    "first_name": "New First",
    "last_name": "New Last"
}
```
**Expected:** Updates both names successfully

### Scenario 3: Update Only First Name
```
POST /api/personal-info/update/
Body: {
    "rider_id": "12345678",
    "first_name": "Only First Updated"
}
```
**Expected:** Updates only first name, last name remains unchanged

### Scenario 4: Update Only Last Name
```
POST /api/personal-info/update/
Body: {
    "rider_id": "12345678",
    "last_name": "Only Last Updated"
}
```
**Expected:** Updates only last name, first name remains unchanged

### Scenario 5: Error - No Fields
```
POST /api/personal-info/update/
Body: {
    "rider_id": "12345678"
}
```
**Expected:** Error message about required fields

### Scenario 6: Error - Empty Names
```
POST /api/personal-info/update/
Body: {
    "rider_id": "12345678",
    "first_name": "",
    "last_name": "   "
}
```
**Expected:** Validation errors for empty names

---

## Integration with Profile Screen

### Frontend Implementation Example:

```javascript
// Load personal information when profile screen opens
async function loadPersonalInfo(riderId) {
    try {
        const response = await fetch('/api/personal-info/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rider_id: riderId
            })
        });
        const data = await response.json();
        
        // Populate form fields
        document.getElementById('firstName').value = data.first_name;
        document.getElementById('lastName').value = data.last_name;
        document.getElementById('username').value = data.username; // read-only
        document.getElementById('email').value = data.email; // read-only
    } catch (error) {
        console.error('Error loading personal info:', error);
    }
}

// Update personal information when user saves
async function updatePersonalInfo(riderId, firstName, lastName) {
    try {
        const response = await fetch('/api/personal-info/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                rider_id: riderId,
                first_name: firstName,
                last_name: lastName
            })
        });
        
        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            // Update UI with new data
            loadPersonalInfo(riderId);
        } else {
            console.error('Update failed:', result);
        }
    } catch (error) {
        console.error('Error updating personal info:', error);
    }
}
```

---

## Key Features:

✅ **Separate APIs** for get and update operations
✅ **Read-only fields** (username, email) cannot be changed
✅ **Editable fields** (first_name, last_name) can be updated
✅ **Partial updates** supported (update only one field)
✅ **Validation** for empty names and length limits
✅ **Proper error handling** with descriptive messages
✅ **Consistent response format** across both APIs