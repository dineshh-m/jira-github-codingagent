# Database Access Layer

## Eloquent ORM

**Model Setup:**
```php
class Post extends Model
{
    use HasFactory, SoftDeletes;
    protected $fillable = ['title', 'slug', 'body', 'status'];
    protected $casts = ['published_at' => 'datetime'];
}
```

## Relationships

**One-to-Many:**
```php
// Post → User
$this->belongsTo(User::class, 'author_id')
$this->hasMany(Post::class, 'author_id')
```

**Many-to-Many:**
```php
$this->belongsToMany(Category::class, 'post_category')
// Pivot: post_category (post_id, category_id)
```

**Usage:**
```php
$post->author                    // Get author
$post->categories                // Get categories
$post->categories()->attach([1,2])  // Attach
$post->categories()->sync([1,2])    // Sync (replace)
```

## Eager Loading

**Problem:** N+1 queries
```php
// Bad
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->author->name; // N queries
}
```

**Solution:** Eager load
```php
// Good
$posts = Post::with(['author', 'categories', 'tags'])->get();
```

## Query Scopes

```php
// In Model
public function scopePublished($query) {
    return $query->where('status', 'published')
                 ->whereNotNull('published_at')
                 ->where('published_at', '<=', now());
}

// Usage
Post::published()->get()
Post::published()->search('laravel')->get()
```

## Common Queries

```php
// Basic
Post::find(1)
Post::findOrFail(1)  // 404 if not found
Post::where('status', 'published')->get()

// Where Has
Post::whereHas('categories', function ($q) {
    $q->where('slug', 'tech');
})->get()

// With Count
Category::withCount('posts')->get()
// Access: $category->posts_count

// Ordering
Post::orderBy('created_at', 'desc')->get()
Post::latest()->get()
```

## Pagination

```php
$posts = Post::with('author')
             ->published()
             ->paginate(20);

// Response
return response()->json([
    'data' => $posts->items(),
    'meta' => [
        'current_page' => $posts->currentPage(),
        'last_page' => $posts->lastPage(),
        'per_page' => $posts->perPage(),
        'total' => $posts->total(),
    ],
]);
```

## Migrations

```php
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->string('slug')->unique();
    $table->text('body');
    $table->enum('status', ['draft', 'published'])->default('draft');
    $table->foreignId('author_id')->constrained('users');
    $table->timestamp('published_at')->nullable();
    $table->timestamps();
    $table->softDeletes();
});
```

**Common Types:**
- `string()`, `text()`, `longText()`
- `integer()`, `boolean()`
- `enum()`, `timestamp()`
- `foreignId()->constrained()`
- `timestamps()`, `softDeletes()`

## Soft Deletes

```php
use SoftDeletes;

$post->delete();        // Soft delete
$post->restore();       // Restore
$post->forceDelete();   // Permanent delete
Post::withTrashed()->get();
Post::onlyTrashed()->get();
```

## Factories & Seeders

```php
// Factory
Post::factory()->create();
Post::factory()->count(10)->create();
Post::factory()->published()->create();

// Seeder
Post::factory()->count(50)->create()->each(function ($post) {
    $post->categories()->attach(
        Category::inRandomOrder()->take(rand(1, 3))->pluck('id')
    );
});
```

## Performance

- **Indexes:** `$table->index('status')`
- **Select specific columns:** `Post::select('id', 'title')->get()`
- **Chunk large datasets:** `Post::chunk(100, function ($posts) { ... })`
- **Always eager load:** Prevent N+1 queries
