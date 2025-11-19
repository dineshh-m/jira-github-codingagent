# CRUD API Specification

## Base URL

```
/api/v1/admin/{resource}  (admin endpoints)
/api/v1/public/{resource} (public endpoints)
```

## Standard Operations

| Method | Endpoint | Purpose | Status |
|--------|----------|---------|--------|
| GET | `/admin/{resource}` | List (paginated) | 200 |
| GET | `/admin/{resource}/{id}` | Show single | 200/404 |
| POST | `/admin/{resource}` | Create | 201/422 |
| PUT | `/admin/{resource}/{id}` | Update | 200/404/422 |
| DELETE | `/admin/{resource}/{id}` | Delete | 200/404 |

## Request/Response Format

**List Response:**
```json
{
  "data": [...],
  "meta": { "current_page": 1, "last_page": 5, "per_page": 20, "total": 100 }
}
```

**Single Resource:**
```json
{
  "data": { "id": 1, "title": "...", ... },
  "message": "Operation successful" // Optional
}
```

**Error (422):**
```json
{
  "message": "The given data was invalid.",
  "errors": { "field": ["Error message"] }
}
```

## Query Parameters

- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20)
- `search` - Search query
- `status` - Filter by status
- Resource-specific filters (`category`, `tag`, etc.)

## Custom Actions

**Publish/Unpublish:**
- `PATCH /admin/{resource}/{id}/publish`
- `PATCH /admin/{resource}/{id}/unpublish`

## Status Codes

- `200` - Success (GET, PUT, DELETE)
- `201` - Created (POST)
- `401` - Unauthenticated
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Server Error

## Headers

```
Content-Type: application/json
Accept: application/json
X-XSRF-TOKEN: {token}
Cookie: XSRF-TOKEN={token}; cms_session={session}
```

## Relationships

**Request:** `{ "category_ids": [1, 2], "tag_ids": [3, 4] }`  
**Response:** Includes `categories` and `tags` arrays

## Validation Rules

- Required: `required`
- String: `string|max:255`
- Unique: `unique:table,column,except,idColumn`
- Array: `array`
- Array items: `array.*:exists:table,id`
- Enum: `in:value1,value2`
