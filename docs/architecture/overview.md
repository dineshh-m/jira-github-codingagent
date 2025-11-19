# Architecture Overview

## System Architecture

```
React Frontend (5173) → Laravel API (8000) → MySQL (3306)
```

**Stack:** React 18 + React Query + Laravel 10 + MySQL 8.0 + Docker

## Project Structure

```
backend/app/Http/Controllers/Api/    # API controllers
backend/app/Models/                    # Eloquent models
backend/routes/api.php                 # API routes
frontend/src/components/                # UI components
frontend/src/pages/                     # Page components
frontend/src/services/                 # API services
frontend/src/contexts/                 # React contexts
```

## Key Patterns

### API Design
- RESTful: `/api/v1/admin/{resource}`
- Response: `{ data: {...}, meta: {...}, message: "..." }`
- Auth: Laravel Sanctum (session-based, CSRF)

### Frontend Layers
1. **Components** - UI (no API calls)
2. **Services** - API communication
3. **React Query** - Server state caching
4. **Context** - Auth state

### Backend Layers
1. **Routes** - URL mapping + middleware
2. **Controllers** - Request handling + validation
3. **Models** - Business logic + relationships
4. **Database** - Eloquent ORM

## Authentication Flow

1. Frontend requests CSRF cookie: `GET /sanctum/csrf-cookie`
2. Login: `POST /api/v1/login` (with CSRF token)
3. Session cookie set automatically
4. Subsequent requests include cookie

## Data Flow

**Read:** Component → useQuery → Service → API → Controller → Model → DB  
**Write:** Component → useMutation → Service → API → Controller → Model → DB → Invalidate Cache

## Security Layers

1. Route protection (ProtectedRoute component)
2. CSRF tokens (Sanctum)
3. Session authentication (cookies)
4. Backend authorization (middleware + policies)
5. Input validation (Laravel validation)

## Performance

- React Query caching (reduces API calls)
- Eager loading (`with()` prevents N+1)
- Pagination (10-20 items per page)
- Debounced search (500ms delay)
