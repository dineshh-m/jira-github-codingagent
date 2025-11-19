# React State Management

## State Types

**1. Server State** - React Query (API data, caching)  
**2. Client State** - Context (auth, preferences)  
**3. Local State** - useState (forms, UI state)

## React Query (Server State)

**Setup:**
```jsx
<QueryClientProvider client={queryClient}>
  <App />
</QueryClientProvider>
```

**Query (Read):**
```jsx
const { data, isLoading, error } = useQuery({
  queryKey: ['admin-posts', page, status],
  queryFn: () => postService.getAdminPosts({ page, status }),
});
```

**Mutation (Write):**
```jsx
const mutation = useMutation({
  mutationFn: (data) => postService.createPost(data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['admin-posts'] });
  },
});
```

**Query Keys:**
```javascript
['admin-posts', page, status, search]
['admin-post', id]
['public-posts', category, tag]
```

## Context (Client State)

**Auth Context:**
```jsx
const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  
  const login = async (email, password) => {
    const data = await authService.login(email, password);
    setUser(data.data.user);
  };
  
  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

**Usage:**
```jsx
const { user, isAuthenticated } = useAuth();
```

## Local State (useState)

```jsx
const [formData, setFormData] = useState({
  title: '',
  body: '',
});

const handleChange = (e) => {
  setFormData(prev => ({
    ...prev,
    [e.target.name]: e.target.value,
  }));
};
```

## Cache Invalidation

```jsx
// After mutations
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ['admin-posts'] });
}
```

## Debouncing

```jsx
const [search, setSearch] = useState('');
const [debouncedSearch, setDebouncedSearch] = useState('');

useEffect(() => {
  const timer = setTimeout(() => {
    setDebouncedSearch(search);
  }, 500);
  return () => clearTimeout(timer);
}, [search]);
```

## Best Practices

- React Query for all API data
- Context only for global client state (auth)
- useState for local component state
- Invalidate cache after mutations
- Use consistent query keys
- Debounce search inputs
