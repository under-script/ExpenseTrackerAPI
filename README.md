# Blogging Platform API

This is an example API for a blogging platform using Django REST Framework.

## Endpoints

### 1. POST /posts/

Create a new post.

#### Request:

```json
{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": 1,
  "tags": [
    1,
    2
  ]
}
```

#### Response:

```json
{
  "id": 1,
  "tags": [
    1,
    2
  ],
  "created": "2024-10-05T15:36:25.339382+05:00",
  "modified": "2024-10-05T15:36:25.339541+05:00",
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": 1
}
```

### 2. PATCH /posts/{id}/

Update an existing post.

#### Request:

```json
{
  "title": "My Updated Blog Post"
}
```

#### Response:

```json
{
  "id": 1,
  "tags": [
    1,
    2
  ],
  "created": "2024-10-05T15:36:25.339382+05:00",
  "modified": "2024-10-05T15:39:01.936293+05:00",
  "title": "My Updated Blog Post",
  "content": "This is the content of my first blog post.",
  "category": 1
}
```

### 3. GET /posts/{id}/

Retrieve a specific post.

#### Response:

```json
{
  "id": 1,
  "tags": [
    {
      "id": 1,
      "name": "Tech"
    },
    {
      "id": 2,
      "name": "Programming"
    }
  ],
  "created": "2024-10-05T15:36:25.339382+05:00",
  "modified": "2024-10-05T15:39:01.936293+05:00",
  "title": "My Updated Blog Post",
  "content": "This is the content of my first blog post.",
  "category": 1
}
```

### 4. GET /posts/

List all posts.

#### Response:

```json
[
  {
    "id": 1,
    "tags": [
      1,
      2
    ],
    "created": "2024-10-05T15:36:25.339382+05:00",
    "modified": "2024-10-05T15:39:01.936293+05:00",
    "title": "My Updated Blog Post",
    "content": "This is the content of my first blog post.",
    "category": 1
  },
  {
    "id": 2,
    "tags": [
      1,
      2
    ],
    "created": "2024-10-05T15:41:07.708386+05:00",
    "modified": "2024-10-05T15:41:07.708468+05:00",
    "title": "My Second Blog Post",
    "content": "This is the content of my second blog post.",
    "category": 1
  }
]
```

### 5. GET /posts?term=second

Search for posts containing a term.

#### Response:

```json
[
  {
    "id": 2,
    "tags": [
      1,
      2
    ],
    "created": "2024-10-05T15:41:07.708386+05:00",
    "modified": "2024-10-05T15:41:07.708468+05:00",
    "title": "My Second Blog Post",
    "content": "This is the content of my second blog post.",
    "category": 1
  }
]
```

<details>
  <summary>Click me</summary>

## Other endpoints

### 1. POST /tags/

Create a new tag.

#### Request:

```json
{
  "name": "Tech"
}
```

#### Response:

```json
{
  "id": 1,
  "name": "Tech"
}
```

### 1. POST /categories/

Create a new category.

#### Request:

```json
{
  "name": "Technology"
}
```

#### Response:

```json
{
  "id": 1,
  "name": "Technology"
}
```

</details>