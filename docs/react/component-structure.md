# React Component Structure

## Organization

```
src/
├── components/     # Reusable UI (Button, Input)
├── pages/          # Page components (PostsList, PostForm)
├── contexts/       # React contexts (AuthContext)
└── services/       # API services
```

## Component Types

**1. Presentational** - Display UI, receive props
```jsx
export const Button = ({ children, variant = 'primary', onClick }) => {
  return <button onClick={onClick}>{children}</button>;
};
```

**2. Container** - Handle data, state, logic
```jsx
export const PostsList = () => {
  const { data, isLoading } = useQuery(...);
  const deleteMutation = useMutation(...);
  return <div>{/* Render */}</div>;
};
```

**3. Layout** - Page structure
```jsx
export const AdminLayout = () => {
  return (
    <div>
      <nav>...</nav>
      <Outlet />
    </div>
  );
};
```

## Component Template

```jsx
export const ComponentName = ({ prop1, prop2 }) => {
  // 1. Hooks
  const [state, setState] = useState(null);
  const { data } = useQuery(...);
  
  // 2. Handlers
  const handleClick = () => { ... };
  
  // 3. Effects
  useEffect(() => { ... }, []);
  
  // 4. Early returns
  if (isLoading) return <LoadingSpinner />;
  
  // 5. Render
  return <div>...</div>;
};
```

## Patterns

**Conditional Rendering:**
```jsx
{isLoading ? <Spinner /> : <Content />}
{error && <ErrorDisplay />}
```

**List Rendering:**
```jsx
{posts?.map((post) => (
  <PostCard key={post.id} post={post} />
))}
```

**Form Handling:**
```jsx
const [formData, setFormData] = useState({ title: '', body: '' });

const handleChange = (e) => {
  setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
};
```

## File Naming

- Files: PascalCase (`PostsList.jsx`)
- Components: PascalCase (`PostsList`)
- Match file name to component name

## Best Practices

- Single responsibility per component
- Use props for configuration
- Extract logic to hooks when complex
- Use semantic HTML
- Keep components focused (< 200 lines)
