# Error Handling

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | GET, PUT, DELETE success |
| 201 | Created | POST success |
| 400 | Bad Request | Invalid request |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation errors |
| 500 | Server Error | Server error |

## Validation Errors (422)

**Automatic:**
```php
$validated = $request->validate([
    'title' => 'required|string|max:255',
]);
// Returns 422 with errors if validation fails
```

**Response:**
```json
{
  "message": "The given data was invalid.",
  "errors": {
    "title": ["The title field is required."]
  }
}
```

## Model Not Found (404)

```php
$post = Post::findOrFail($id);
// Automatically returns 404 if not found
```

## Authentication Errors

**401 Unauthorized:**
```json
{ "message": "Unauthenticated." }
```

**403 Forbidden:**
```php
abort(403, 'This action is unauthorized.');
```

## Error Response Format

```json
{
  "message": "Error description",
  "errors": {
    "field": ["Error message"]
  }
}
```

## Common Scenarios

| Scenario | Status | Response |
|----------|--------|----------|
| Validation fails | 422 | `{ message, errors }` |
| Resource not found | 404 | `{ message }` |
| Not authenticated | 401 | `{ message: "Unauthenticated." }` |
| Forbidden | 403 | `{ message: "This action is unauthorized." }` |
| Unique constraint | 422 | Validation error on field |
| Foreign key violation | 500 | Database error |

## Frontend Handling

**Axios Interceptor:**
```javascript
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.dispatchEvent(new CustomEvent('unauthorized'));
    }
    return Promise.reject(error);
  }
);
```

**Component:**
```javascript
onError: (error) => {
  if (error.response?.data?.errors) {
    setErrors(error.response.data.errors); // Validation
  } else if (error.response?.status === 401) {
    navigate('/login'); // Unauthorized
  }
}
```

## Best Practices

- Always validate input
- Use appropriate status codes
- Provide clear error messages
- Log errors for debugging
- Don't expose sensitive info in production
- Handle edge cases
- Use `findOrFail()` for automatic 404
