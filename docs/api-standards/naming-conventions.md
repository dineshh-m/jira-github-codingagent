# API Naming Conventions

## URL Structure

```
/api/v1/{namespace}/{resource}/{identifier}/{action}
```

**Patterns:**
- Version: `/v1`, `/v2`
- Namespace: `/public` (no auth), `/admin` (auth required)
- Resource: Plural lowercase (`posts`, `categories`)
- Identifier: ID (admin) or slug (public)
- Action: Custom actions (`publish`, `unpublish`)

## Naming Rules

| Type | Convention | Example |
|------|------------|---------|
| Resources | Plural lowercase | `posts`, `categories` |
| JSON Fields | snake_case | `author_id`, `published_at` |
| Foreign Keys | `{resource}_id` | `author_id`, `category_id` |
| Arrays | `{resource}_ids` | `category_ids`, `tag_ids` |
| Timestamps | `{action}_at` | `created_at`, `published_at` |
| URLs | `{resource}_url` | `cover_image_url` |
| Query Params | snake_case | `per_page`, `category` |

## Controller Methods

| Action | Method Name |
|--------|-------------|
| List (public) | `index()` |
| List (admin) | `adminIndex()` |
| Show (public) | `show($slug)` |
| Show (admin) | `adminShow($id)` |
| Create | `store(Request $request)` |
| Update | `update(Request $request, $id)` |
| Delete | `destroy($id)` |

## Service Methods (Frontend)

**Pattern:** `{verb}{Resource}({params})`

```javascript
getAdminPosts(params)
getAdminPost(id)
createPost(data)
updatePost(id, data)
deletePost(id)
publishPost(id)
```

## React Query Keys

**Pattern:** `['{namespace}-{resource}', ...filters]`

```javascript
['admin-posts', page, status, search]
['admin-post', id]
['public-posts', category, tag]
```

## Component Names

- Files: PascalCase (`PostsList.jsx`, `Button.jsx`)
- Components: PascalCase (`PostsList`, `Button`)
- Variables: camelCase (`formData`, `isLoading`)

## Database

- Tables: Plural snake_case (`posts`, `post_category`)
- Models: Singular PascalCase (`Post`, `Category`)
- Columns: snake_case (`author_id`, `published_at`)
