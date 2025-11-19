# Laravel Core Patterns

## MVC Structure

```
Route → Controller → Model → Database
```

## Controller Pattern

```php
class PostController extends Controller
{
    // Public
    public function index(Request $request) { ... }
    public function show($slug) { ... }
    
    // Admin
    public function adminIndex(Request $request) { ... }
    public function adminShow($id) { ... }
    public function store(Request $request) { ... }
    public function update(Request $request, $id) { ... }
    public function destroy($id) { ... }
}
```

**Responsibilities:** Validate input, delegate to models, return JSON

## Model Pattern

```php
class Post extends Model
{
    protected $fillable = ['title', 'slug', 'body', 'status', 'author_id'];
    protected $casts = ['published_at' => 'datetime'];
    
    // Relationships
    public function author() {
        return $this->belongsTo(User::class, 'author_id');
    }
    
    // Scopes
    public function scopePublished($query) {
        return $query->where('status', 'published')
                     ->whereNotNull('published_at')
                     ->where('published_at', '<=', now());
    }
}
```

## Relationships

**One-to-Many:**
```php
// Post belongs to User
$this->belongsTo(User::class, 'author_id')

// User has many Posts
$this->hasMany(Post::class, 'author_id')
```

**Many-to-Many:**
```php
$this->belongsToMany(Category::class, 'post_category')
```

**Eager Loading:**
```php
Post::with(['author', 'categories', 'tags'])->get()
```

## Query Scopes

```php
// In Model
public function scopePublished($query) { ... }
public function scopeSearch($query, $search) { ... }

// Usage
Post::published()->search('laravel')->get()
```

## Validation

```php
$validated = $request->validate([
    'title' => 'required|string|max:255',
    'slug' => 'nullable|string|unique:posts,slug',
    'status' => 'required|in:draft,published',
    'category_ids' => 'nullable|array',
    'category_ids.*' => 'exists:categories,id',
]);
```

**Update:** Use `sometimes` for partial updates

## Response Format

```php
// Single
return response()->json(['data' => $post]);

// Collection
return response()->json([
    'data' => $posts->items(),
    'meta' => [
        'current_page' => $posts->currentPage(),
        'last_page' => $posts->lastPage(),
        'per_page' => $posts->perPage(),
        'total' => $posts->total(),
    ],
]);

// With message
return response()->json([
    'data' => $post,
    'message' => 'Post created successfully',
], 201);
```

## Routes

```php
Route::prefix('v1')->group(function () {
    Route::prefix('public')->group(function () {
        Route::get('/posts', [PostController::class, 'index']);
    });
    
    Route::prefix('admin')->middleware(['auth:sanctum'])->group(function () {
        Route::get('/posts', [PostController::class, 'adminIndex']);
        Route::post('/posts', [PostController::class, 'store']);
        // ...
    });
});
```

## Best Practices

- Thin controllers, fat models
- Always eager load relationships
- Use query scopes for reusable logic
- Validate all input
- Return consistent JSON format
- Use type hints
