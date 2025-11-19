# API Consumption

## Service Layer

**Structure:**
```javascript
// services/api.js - Axios instance
const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  withCredentials: true,
});

// services/postService.js
export const postService = {
  async getAdminPosts(params) {
    const response = await api.get('/admin/posts', { params });
    return response.data;
  },
  async createPost(data) {
    const response = await api.post('/admin/posts', data);
    return response.data;
  },
};
```

## CSRF Handling

**Request Interceptor:**
```javascript
api.interceptors.request.use(async (config) => {
  if (['post', 'put', 'patch', 'delete'].includes(config.method)) {
    await getCsrfToken();
    const token = getCookie('XSRF-TOKEN');
    if (token) config.headers['X-XSRF-TOKEN'] = token;
  }
  return config;
});
```

**Response Interceptor:**
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

## Using Services

**With React Query:**
```jsx
// Query
const { data, isLoading } = useQuery({
  queryKey: ['admin-posts'],
  queryFn: () => postService.getAdminPosts(),
});

// Mutation
const mutation = useMutation({
  mutationFn: (data) => postService.createPost(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['admin-posts'] });
  },
  onError: (error) => {
    if (error.response?.data?.errors) {
      setErrors(error.response.data.errors);
    }
  },
});
```

## Error Handling

**Response Structure:**
```json
// 422 Validation
{ "message": "...", "errors": { "field": ["Error"] } }

// 404 Not Found
{ "message": "Resource not found" }

// 401 Unauthorized
{ "message": "Unauthenticated." }
```

**Handling:**
```javascript
onError: (error) => {
  if (error.response?.status === 422) {
    setErrors(error.response.data.errors); // Validation
  } else if (error.response?.status === 401) {
    navigate('/login'); // Unauthorized
  }
}
```

## Request Patterns

**GET:**
```javascript
postService.getAdminPosts({ page: 1, status: 'published' })
```

**POST:**
```javascript
postService.createPost({ title: '...', body: '...' })
```

**PUT:**
```javascript
postService.updatePost(id, { title: '...' })
```

**DELETE:**
```javascript
postService.deletePost(id)
```

**PATCH:**
```javascript
postService.publishPost(id)
```

## Best Practices

- Always use services (don't call `api.get()` directly)
- Use React Query for all data fetching
- Handle loading and error states
- Invalidate cache after mutations
- Use consistent query keys
- Handle validation errors at field level
