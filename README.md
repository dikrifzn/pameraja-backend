# 💼 PamerAja API

API ini dibuat menggunakan Django & Django REST Framework untuk mengelola pengguna, media sosial, proyek, komentar, dan fitur interaksi lainnya. Dokumentasi ini mengikuti struktur collection Postman yang telah disiapkan.

## 🌐 Base URL

```
{{base_url}} = http://127.0.0.1:8000/api
```

## 🔐 Authentication

### 1. Register

* **Endpoint:** `POST {{base_url}}/auth/register/`
* **Headers:** `Content-Type: application/json`
* **Body:**

```json
{
  "username": "testuser",
  "password": "testpassword",
  "email": "test@example.com"
}
```

* **Response:**

```json
{
  "status": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

### 2. Login

* **Endpoint:** `POST {{base_url}}/auth/login/`
* **Body:**

```json
{
  "username": "testuser",
  "password": "testpassword"
}
```

* **Response:**

```json
{
  "status": true,
  "message": "Login successful",
  "data": {
    "access": "<JWT_ACCESS_TOKEN>",
    "refresh": "<JWT_REFRESH_TOKEN>"
  }
}
```

### 3. Refresh Token

* **Endpoint:** `POST {{base_url}}/auth/token/refresh/`
* **Body:**

```json
{
  "refresh": "{{refresh_token}}"
}
```

* **Response:**

```json
{
  "status": true,
  "message": "Token refreshed",
  "data": {
    "access": "<NEW_ACCESS_TOKEN>"
  }
}
```

### 4. Logout

* **Endpoint:** `POST {{base_url}}/auth/logout/`
* **Headers:** `Authorization: Bearer {{access_token}}`
* **Body:**

```json
{
  "refresh": "{{refresh_token}}"
}
```

* **Response:**

```json
{
  "status": true,
  "message": "Successfully logged out"
}
```

---

## 👤 User Profile

### 5. Get Profile

* **Endpoint:** `GET {{base_url}}/users/`
* **Headers:** `Authorization: Bearer {{access_token}}`
* **Response:**

```json
{
  "status": true,
  "message": "User profile retrieved",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "position": "CEO",
    "address": "Jl. Veteran No. 140"
  }
}
```

### 6. Update Profile

* **Endpoint:** `PUT {{base_url}}/users/`
* **Headers:** `Authorization: Bearer {{access_token}}`
* **Body:**

```json
{
  "username": "updateduser",
  "email": "userupdate@gmail.com",
  "position": "Designer",
  "address": "Jl. Baru"
}
```

* **Response:**

```json
{
  "status": true,
  "message": "User profile updated successfully",
  "data": {
    "username": "updateduser",
    "email": "userupdate@gmail.com",
    "position": "Designer",
    "address": "Jl. Baru"
  }
}
```

### 7. Delete Profile

* **Endpoint:** `DELETE {{base_url}}/users/`
* **Headers:** `Authorization: Bearer {{access_token}}`
* **Response:**

```json
{
  "status": true,
  "message": "User deleted successfully"
}
```

---

## 🌐 Social Media

### 8. Get Social Media

* **Endpoint:** `GET {{base_url}}/users/social-media/`
* **Headers:** `Authorization: Bearer {{access_token}}`
* **Response:**

```json
{
  "status": true,
  "message": "Social media retrieved",
  "data": [
    {
      "id": 1,
      "name": "Instagram",
      "url": "https://instagram.com/testuser"
    }
  ]
}
```

### 9. Create Social Media

* **Endpoint:** `POST {{base_url}}/users/social-media/`
* **Body:**

```json
{
  "name": "Instagram",
  "url": "https://instagram.com/testuser"
}
```

* **Response:**

```json
{
  "status": true,
  "message": "Social media created",
  "data": {
    "id": 1,
    "name": "Instagram",
    "url": "https://instagram.com/testuser"
  }
}
```

### 10. Update Social Media

* **Endpoint:** `PUT {{base_url}}/users/social-media/{id}/`
* **Body:**

```json
{
  "name": "Updated IG",
  "url": "https://instagram.com/updateduser"
}
```

### 11. Delete Social Media

* **Endpoint:** `DELETE {{base_url}}/users/social-media/{id}/`

---

## 📁 Project

### 12. Create Project

* **Endpoint:** `POST {{base_url}}/projects/`
* **Headers:** `Content-Type: multipart/form-data`
* **Body (Form Data):**

  * `title`: "My Project"
  * `description`: "Project description"
  * `category`: "Design"
  * `image_url`: (file)
* **Response:**

```json
{
  "status": true,
  "message": "Project created successfully",
  "data": {
    "id": 1,
    "title": "My Project",
    "description": "Project description",
    "category": "Design",
    "image_url": "http://..."
  }
}
```

### 13. Update Project

* **Endpoint:** `PUT {{base_url}}/projects/{id}/`
* **Body (Form Data):** sama seperti create
* **Response:**

```json
{
  "status": true,
  "message": "Project updated successfully",
  "data": {
    "id": 1,
    "title": "Updated Project",
    "description": "Updated description",
    "category": "Updated Category",
    "image_url": "http://..."
  }
}
```

### 14. Delete Project

* **Endpoint:** `DELETE {{base_url}}/projects/{id}/`
* **Response:**

```json
{
  "status": true,
  "message": "Project deleted successfully"
}
```

---

## ❤️ Likes

### 15. Add or Remove Like

* **Endpoint:** `POST {{base_url}}/projects/{id}/likes/`

### 16. Get Likes

* **Endpoint:** `GET {{base_url}}/projects/{id}/likes/`
* **Response:**

```json
{
  "status": true,
  "message": "Likes retrieved",
  "data": {
    "likes_count": 5,
    "liked_by": [
      {
        "id": 1,
        "username": "user"
      }
    ]
  }
}
```

---

## 💬 Comments

### 17. Get Comments

* **Endpoint:** `GET {{base_url}}/projects/{id}/comments/`

### 18. Create Comment

* **Endpoint:** `POST {{base_url}}/projects/{id}/comments/`
* **Body:**

```json
{
  "content": "Great project!"
}
```

* **Response:**

```json
{
  "status": true,
  "message": "Comment created",
  "data": {
    "id": 1,
    "content": "Great project!",
    "user": "testuser"
  }
}
```

### 19. Update Comment

* **Endpoint:** `PUT {{base_url}}/comments/{id}/`
* **Body:**

```json
{
  "content": "Updated content"
}
```

### 20. Delete Comment

* **Endpoint:** `DELETE {{base_url}}/comments/{id}/`

---

## 🚧 Database Models

### User

| Field       | Type                |
| ----------- | ------------------- |
| username    | CharField           |
| email       | EmailField (unique) |
| position    | CharField           |
| address     | TextField           |
| image\_url  | ImageField          |
| created\_at | DateTime            |
| edited\_at  | DateTime            |

### SocialMedia

| Field       | Type              |
| ----------- | ----------------- |
| id\_user    | ForeignKey (User) |
| name        | CharField         |
| url         | CharField         |
| created\_at | DateTime          |
| edited\_at  | DateTime          |

### Project

| Field       | Type                 |
| ----------- | -------------------- |
| id\_user    | ForeignKey (User)    |
| title       | CharField            |
| description | TextField            |
| category    | CharField            |
| file\_url   | CharField (optional) |
| image\_url  | ImageField           |
| views       | Integer              |
| created\_at | DateTime             |
| edited\_at  | DateTime             |

### Comment

| Field       | Type                 |
| ----------- | -------------------- |
| id\_user    | ForeignKey (User)    |
| id\_project | ForeignKey (Project) |
| message     | TextField            |
| created\_at | DateTime             |
| edited\_at  | DateTime             |

### Like

| Field       | Type                 |
| ----------- | -------------------- |
| id\_user    | ForeignKey (User)    |
| id\_project | ForeignKey (Project) |

---

## 🛠️ Setup Project Locally

```bash
git clone https://github.com/dikrifzn/pameraja-backend.git
cd pameraja-backend
```
```bash
pip install pipenv
pipenv install
pipenv shell
```
```bash
python manage.py migrate
python manage.py runserver
```

---

## 🧰 Tech Stack

* Django
* Django REST Framework
* JWT Authentication
* PostgreSQL / MySQL (configurable)

---

📮 For more information, check out the [Postman Collection](https://github.com/dikrifzn/pameraja-backend/blob/main/PamerAja%20API.postman_collection.json)

created by [Dikri Fauzan Amrulloh](https://github.com/dikrifzn/pameraja-backend)