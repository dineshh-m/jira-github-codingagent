# Unit Testing Standards

## Test Structure

```
tests/
├── Feature/    # HTTP request/response tests
└── Unit/        # Isolated component tests
```

## Feature Test Pattern

```php
use RefreshDatabase;

class PostTest extends TestCase
{
    public function test_authenticated_user_can_create_post()
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)
            ->postJson('/api/v1/admin/posts', [
                'title' => 'Test Post',
                'body' => 'Content',
                'status' => 'draft',
            ]);
        
        $response->assertStatus(201)
                 ->assertJsonStructure(['data', 'message']);
        
        $this->assertDatabaseHas('posts', [
            'title' => 'Test Post',
        ]);
    }
}
```

## Common Assertions

**HTTP:**
```php
$response->assertStatus(200);
$response->assertJsonStructure(['data', 'meta']);
$response->assertJson(['data' => ['title' => 'Test']]);
$response->assertJsonPath('data.title', 'Test');
```

**Database:**
```php
$this->assertDatabaseHas('posts', ['title' => 'Test']);
$this->assertDatabaseMissing('posts', ['id' => 1]);
$this->assertCount(5, Post::all());
```

**Model:**
```php
$this->assertInstanceOf(User::class, $post->author);
$this->assertTrue($posts->contains($post));
```

## Test Patterns

**Arrange-Act-Assert:**
```php
// Arrange
$user = User::factory()->create();

// Act
$response = $this->actingAs($user)->postJson(...);

// Assert
$response->assertStatus(201);
```

**Authentication:**
```php
$user = User::factory()->create();
$this->actingAs($user)->getJson('/api/v1/admin/posts');
```

**Validation:**
```php
$response->assertStatus(422)
         ->assertJsonValidationErrors(['title', 'body']);
```

**404:**
```php
$response = $this->getJson('/api/v1/admin/posts/99999');
$response->assertStatus(404);
```

## Unit Test Example

```php
public function test_published_scope_filters_correctly()
{
    $published = Post::factory()->published()->create();
    $draft = Post::factory()->draft()->create();
    
    $results = Post::published()->get();
    
    $this->assertTrue($results->contains($published));
    $this->assertFalse($results->contains($draft));
}
```

## Running Tests

```bash
php artisan test
php artisan test --filter test_name
php artisan test tests/Feature/PostTest.php
```

## Best Practices

- Use descriptive test names: `test_user_can_create_post`
- Use factories for test data
- Use `RefreshDatabase` or `DatabaseTransactions`
- Test both success and failure cases
- Test authentication/authorization
- Test validation errors
- Keep tests focused (one thing per test)
