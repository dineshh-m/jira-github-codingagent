# React Testing Library Patterns

## Philosophy

**Test user behavior, not implementation**

## Setup

```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

## Basic Pattern

```jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('renders button', () => {
  render(<Button>Click me</Button>);
  expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
});
```

## Query Priority

1. `getByRole` - Most accessible
2. `getByLabelText` - Form inputs
3. `getByText` - Text content
4. `getByTestId` - Last resort

## User Interactions

```jsx
const user = userEvent.setup();

// Click
await user.click(screen.getByRole('button'));

// Type
await user.type(screen.getByLabelText(/email/i), 'test@example.com');

// Submit form
await user.click(screen.getByRole('button', { name: /submit/i }));
```

## Testing with React Query

```jsx
const renderWithQuery = (component) => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      {component}
    </QueryClientProvider>
  );
};

test('displays posts', async () => {
  jest.spyOn(postService, 'getAdminPosts').mockResolvedValue({
    data: [{ id: 1, title: 'Post 1' }],
  });

  renderWithQuery(<PostsList />);

  await waitFor(() => {
    expect(screen.getByText('Post 1')).toBeInTheDocument();
  });
});
```

## Async Testing

```jsx
import { waitFor } from '@testing-library/react';

await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});
```

## Error States

```jsx
test('displays error', async () => {
  jest.spyOn(service, 'method').mockRejectedValue(new Error('Failed'));

  render(<Component />);

  await waitFor(() => {
    expect(screen.getByText(/error/i)).toBeInTheDocument();
  });
});
```

## Best Practices

- Test what users see and do
- Use accessible queries (`getByRole`, `getByLabelText`)
- Wait for async operations (`waitFor`)
- Mock external dependencies (services, context)
- Test loading, success, and error states
- Keep tests focused (one thing per test)
